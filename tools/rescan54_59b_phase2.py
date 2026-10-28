#!/usr/bin/env python3
# rescan54_59b_phase2.py — Task 54-59, фаза 2: OP (near=1) для ШЕСТИ NEW (вспышка 10:53-11:29):
# 196646 «Когда клановые воины получат вторую жизнь?» (cc=8, 11:29), 196643 «Моя борьба (с оптимизацией)»
# (cc=12, 11:28), 196640 «забанят ли за багаюз в данже?» (cc=20, 11:28), 196644 «баг с сворачиванием игры»
# (cc=10, 11:20), 196642 «Отображение бартера на экране» (cc=2, 10:58), 196641 «Размышления по пакерству» (cc=2, 10:53).
import json, os, urllib.request, time, datetime, re

TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
NEW = [196646, 196643, 196640, 196644, 196642, 196641]

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
        print(f'OK {name} ({len(body)}B)')
        return True
    except Exception as e:
        print(f'FAIL {name}: {e}')
        return False

def head_text(p, n=240):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or a.get('contentHtml') or ''
    if not isinstance(t, str): t = str(t)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()[:n]

for tid in NEW:
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)
    try:
        d = json.load(open(os.path.join(OUT, f'discussion_{tid}_near1_{TS}.json')))
        aa = d.get('data', {}).get('attributes', {})
        users = {u['id']: u['attributes'].get('username') for u in (d.get('included') or []) if u.get('type') == 'users'}
        print(f"[{tid}] cc={aa.get('commentCount')} LPN={aa.get('lastPostNumber')} title={aa.get('title','')[:70]} created={aa.get('createdAt','')[:16]}")
        posts = [i for i in (d.get('included') or []) if isinstance(i, dict) and i.get('type') == 'posts']
        for p in sorted(posts, key=lambda x: x.get('attributes', {}).get('number') or 0)[:3]:
            a = p.get('attributes', {})
            uid = (p.get('relationships', {}).get('user', {}) or {}).get('data', {}).get('id')
            print(f"  #{a.get('number')} {a.get('createdAt','')[:16]} [{users.get(uid,'?')}] :: {head_text(p)}")
    except Exception as e:
        print(f'[{tid}] parse fail {e}')

print(f'TS={TS}')
