#!/usr/bin/env python3
# phase2_54_129.py — OP near=1 + хвосты near999999 для NEW-тредов патч-волны
import json, os, urllib.request, time, re

TS = '20261021_1045'
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'

def get(url, name):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}'); return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        json.loads(body)
        print(f'OK {name} ({len(body)}B)'); return True
    except Exception as e:
        print(f'FAIL {name}: {e}'); return False

def head_text(p, n=200):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or a.get('contentHtml') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()[:n]

def show(tid, near):
    fn = f'discussion_{tid}_near{near}_{TS}.json'
    d = json.load(open(os.path.join(OUT, fn)))
    aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
    print(f"[{tid}] cc={aa.get('commentCount')} lastPostNumber={aa.get('lastPostNumber')} title={aa.get('title','')[:70]} sticky={aa.get('sticky')}")
    items = [i for i in ([d.get('data')] if isinstance(d.get('data'), dict) else []) + (d.get('included') or [])
             if isinstance(i, dict) and i.get('type') == 'posts']
    tail = sorted(items, key=lambda p: p.get('attributes', {}).get('number') or 0)[-6:]
    for p in tail:
        a = p.get('attributes', {})
        print(f"  #{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")

for tid in (196791, 196794, 196788):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)
    show(tid, 1)
    print('--- tail:')
    show(tid, 999999)
