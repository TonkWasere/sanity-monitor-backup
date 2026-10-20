#!/usr/bin/env python3
# rescan54_113_finisher.py — дозагрузка 33 недостающих loop-хвостов раунда 54-113
# (первый прогон убит таймаутом ВМ на 10-й минуте, 137/170 снапов уже на диске, TS 1731).
# Тот же UA/sleep 1с/JSON-валидация, что в rescan54_113_fetch.py.
import json, os, urllib.request, time, re

TS = '20261020_1731'
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'

MISSING = [196717, 196707, 196638, 196561, 193777, 185811, 196630, 196624, 196623,
           196631, 196633, 196634, 196564, 196635, 196588, 196427, 196637, 196639,
           196625, 196628, 196629, 196150, 174335, 196612, 196618, 196611, 187993,
           196572, 196434, 196382, 179857, 195082, 196223]

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
    out = []
    for i in items:
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    return out

def head_text(p, n=110):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or ''
    if not t:
        t = a.get('contentHtml') or ''
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
        print(f"[{tid}] cc={aa.get('commentCount')} lastPostNumber={aa.get('lastPostNumber')} sticky={aa.get('sticky')} locked={aa.get('isLocked')}")
    except Exception as e:
        print(f'[{tid}] attrs fail {e}')
    tail = sorted(pp, key=lambda p: p.get('attributes', {}).get('number') or 0)[-6:]
    for p in tail:
        a = p.get('attributes', {})
        print(f"  #{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")
    return pp

if __name__ == '__main__':
    ok = fail = 0
    for tid in MISSING:
        if get(f'{BASE}/api/discussions/{tid}?page[near]=999999',
               f'discussion_{tid}_near999999_{TS}.json'):
            ok += 1
        else:
            fail += 1
        thread_summary(tid, near='999999')
        time.sleep(1)
    print(f'\nFINISHER DONE: OK={ok} FAIL={fail} (FAIL = штатные 404-контролы 196707/196717)')
