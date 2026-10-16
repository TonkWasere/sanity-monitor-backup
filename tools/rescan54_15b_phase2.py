#!/usr/bin/env python3
# rescan54_15b_phase2.py — Task 54-15 phase 2: OP новых тредов 196425 (офиц. сбор фидбека ОТС) /
# 196551 (3д ДШД) + догон хвостов 196537 (cc=28) / 196539 (вылеты).
import json, os, urllib.request, time, datetime, re

TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'

def get(url, name, validate_json=True):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}'); return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        if validate_json:
            json.loads(body)
        print(f'OK {name} ({len(body)}B)')
        return True
    except Exception as e:
        print(f'FAIL {name}: {e}')
        return False

def posts_of(fname):
    try:
        d = json.load(open(os.path.join(OUT, fname)))
    except Exception as e:
        print(f'PARSE FAIL {fname}: {e}'); return []
    data = d.get('data')
    items = data if isinstance(data, list) else [data] if data else []
    out = [i for i in items if isinstance(i, dict) and i.get('type') == 'posts']
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    return out

def head_text(p, n=160):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

def thread_summary(tid, near='999999'):
    fn = f'discussion_{tid}_near{near}_{TS}.json'
    pp = posts_of(fn)
    try:
        dd = json.load(open(os.path.join(OUT, fn)))
        aa = dd.get('data', {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
        print(f"[{tid}] cc={aa.get('commentCount')} lastPostNumber={aa.get('lastPostNumber')} title={aa.get('title','')} sticky={aa.get('sticky')} locked={aa.get('isLocked')}")
    except Exception as e:
        print(f'[{tid}] attrs fail {e}')
    tail = sorted(pp, key=lambda p: p.get('attributes', {}).get('number') or 0)[-8:]
    for p in tail:
        a = p.get('attributes', {})
        print(f"  #{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")

for tid, near in ((196425, '1'), (196425, '999999'), (196551, '1'), (196551, '999999'),
                  (196537, '999999'), (196539, '999999')):
    get(f'{BASE}/api/discussions/{tid}?page[near]={near}', f'discussion_{tid}_near{near}_{TS}.json')
    time.sleep(1)

print('\n===== ФАЗА 2 РЕЗЮМЕ =====')
print('--- 196425 ОФИЦ. СБОР ФИДБЕКА ОТС ---')
thread_summary(196425, '1')
thread_summary(196425, '999999')
print('--- 196551 3д ДШД ---')
thread_summary(196551, '1')
thread_summary(196551, '999999')
print('--- 196537 детектор прикопов (был cc=9) ---')
thread_summary(196537, '999999')
print('--- 196539 вылеты (был cc=13) ---')
thread_summary(196539, '999999')

print(f'\nTS={TS}')
