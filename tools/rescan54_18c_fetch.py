#!/usr/bin/env python3
# rescan54_18c_fetch.py — добор OP новых тредов фронта (не было в раунде Task 53): 196461 (Раздутый ттк, cc=147), 196505, 196506, 196497, 196509
import json, os, urllib.request, time, datetime, re

TS = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M')
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

def head_text(p, n=200):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or a.get('contentHtml') or ''
    if not isinstance(t, str):
        t = str(t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

def op_summary(tid):
    fn = f'discussion_{tid}_near1_{TS}.json'
    try:
        dd = json.load(open(os.path.join(OUT, fn)))
        aa = dd.get('data', {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
        print(f"[{tid}] cc={aa.get('commentCount')} LPN={aa.get('lastPostNumber')} createdAt={aa.get('createdAt','')[:16]} title={aa.get('title','')[:60]}")
    except Exception as e:
        print(f'[{tid}] attrs fail {e}')
    pp = posts_of(fn)
    op = next((p for p in pp if p.get('attributes', {}).get('number') == 1), None)
    if op:
        print(f"  OP {op['attributes'].get('createdAt','')[:16]} :: {head_text(op)}")

targets = [(196461, True), (196505, False), (196506, False), (196497, False), (196509, False)]
for tid, with_tail in targets:
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)
    if with_tail:
        get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)
        pp = posts_of(f'discussion_{tid}_near999999_{TS}.json')
        tail = sorted(pp, key=lambda p: p.get('attributes', {}).get('number') or 0)[-4:]
        print(f'--- {tid} хвост ---')
        for p in tail:
            a = p.get('attributes', {})
            print(f"  #{a.get('number')} {a.get('createdAt','')[:16]} :: {head_text(p, 130)}")

print('\n===== OP-резюме новых тредов =====')
for tid, _ in targets:
    op_summary(tid)

print(f'\nTS={TS}')
