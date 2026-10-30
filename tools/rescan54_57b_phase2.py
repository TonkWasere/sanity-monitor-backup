#!/usr/bin/env python3
# rescan54_57b_phase2.py — Task 54-57, фаза 2: OP (near=1) для NEW/воскресших:
# 196635 «Как это работает?» (cc=2, 09:25), 196588 «Нужна помощь» (cc=14, 09:13),
# 196427 «"3 полигона" на клановом паке» (cc=9, некро 09:26).
import json, os, urllib.request, time, datetime, re

TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
NEW = [196635, 196588, 196427]

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

def head_text(p, n=220):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or a.get('contentHtml') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

for tid in NEW:
    fn = f'discussion_{tid}_near1_{TS}.json'
    ok = get(f'{BASE}/api/discussions/{tid}?page[near]=1', fn)
    time.sleep(1)
    if not ok:
        continue
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        aa = d.get('data', {}).get('attributes', {})
        print(f"[{tid}] cc={aa.get('commentCount')} LPN={aa.get('lastPostNumber')} createdAt={aa.get('createdAt','?')[:16]} title={aa.get('title','')[:70]}")
        for i in (d.get('included') or []):
            if isinstance(i, dict) and i.get('type') == 'posts' and i.get('attributes', {}).get('number') == 1:
                a = i.get('attributes', {})
                print(f"  OP #{a.get('number')} {a.get('createdAt')} :: {head_text(i)}")
                break
    except Exception as e:
        print(f'[{tid}] parse fail: {e}')
print(f'TS={TS}')
