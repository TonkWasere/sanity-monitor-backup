#!/usr/bin/env python3
# rescan54_1b_phase2.py — Task 54-1 phase 2: OP новых фронт-тредов (196521/196526/196527) +
# детальный хвост 196524 (Глеб cc=68, window #30+) + контроль удаления #93 в 196424 (снап 00:29).
import json, os, urllib.request, time, re

TS = '20261016_0128'
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
    out = []
    for i in items:
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    return out

def head_text(p, n=170):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or ''
    if not t:
        t = a.get('contentHtml') or ''
    if not isinstance(t, str):
        t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

# === OP новых ===
for tid in (196521, 196526, 196527):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)
    print(f'\n===== OP {tid} =====')
    try:
        d = json.load(open(os.path.join(OUT, f'discussion_{tid}_near1_{TS}.json')))
        aa = d.get('data', {}).get('attributes', {})
        print(f"  title={aa.get('title')} cc={aa.get('commentCount')} createdAt={aa.get('createdAt','')[:19]}")
    except Exception as e:
        print(f'  attrs fail: {e}')
    pp = sorted(posts_of(f'discussion_{tid}_near1_{TS}.json'), key=lambda p: p.get('attributes', {}).get('number') or 0)
    for p in pp[:4]:
        a = p.get('attributes', {})
        print(f"  #{a.get('number')} {a.get('createdAt','')[:19]} :: {head_text(p, 200)}")

# === Глеб 196524: хвост #30-68 (история «разбора полетов») ===
print('\n===== 196524 ГЛЕБ: посты #30+ (кто спалил / долги / акк) =====')
pp = sorted(posts_of(f'discussion_196524_near999999_{TS}.json'), key=lambda p: p.get('attributes', {}).get('number') or 0)
for p in pp:
    n = p.get('attributes', {}).get('number') or 0
    if n >= 30:
        print(f"  #{n} {p.get('attributes',{}).get('createdAt','')[:19]} :: {head_text(p)}")

# === 196424: сверка удаления #93 со снапом 00:29 ===
print('\n===== 196424 ОТС: сверка снапов =====')
try:
    old = json.load(open(os.path.join(OUT, 'discussion_196424_near999999_20261016_0029.json')))
    oldaa = old.get('data', {}).get('attributes', {})
    oldnums = sorted((p.get('attributes', {}).get('number') or 0) for p in posts_of('discussion_196424_near999999_20261016_0029.json'))
    print(f"снап 00:29: cc={oldaa.get('commentCount')} LPN={oldaa.get('lastPostNumber')} живые посты до #{max(oldnums) if oldnums else '?'}")
except Exception as e:
    print(f'old snap fail: {e}')
try:
    new = json.load(open(os.path.join(OUT, f'discussion_196424_near999999_{TS}.json')))
    newaa = new.get('data', {}).get('attributes', {})
    newnums = sorted((p.get('attributes', {}).get('number') or 0) for p in posts_of(f'discussion_196424_near999999_{TS}.json'))
    print(f"снап 01:28: cc={newaa.get('commentCount')} LPN={newaa.get('lastPostNumber')} живые посты до #{max(newnums) if newnums else '?'}")
    print('>>> #93 (00:09, негатив по «испытаниям» ОТС) был в снапе 00:29 и ОТСУТСТВУЕТ в 01:28 → УДАЛЁН модерацией' if 93 not in newnums and 93 in oldnums else '>>> #93 статус: не подтверждено удаление (проверить вручную)')
except Exception as e:
    print(f'new snap fail: {e}')
