#!/usr/bin/env python3
# rescan54_55b_phase2.py — Task 54-55, фаза 2: OP (near=1) для NEW-тредов 196633/196634.
import json, os, urllib.request, time, datetime, re

TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
NEW = [196633, 196634]

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

def head_text(p, n=200):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or a.get('contentHtml') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()[:n]

for tid in NEW:
    fn = f'discussion_{tid}_near1_{TS}.json'
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', fn); time.sleep(1)
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        aa = d.get('data', {}).get('attributes', {})
        print(f"[{tid}] title={aa.get('title')!r} cc={aa.get('commentCount')} LPN={aa.get('lastPostNumber')} createdAt={aa.get('createdAt')}")
        print(f"  tags={[t.get('attributes', {}).get('name') if isinstance(t, dict) else t for t in (d.get('included') or []) if isinstance(t, dict) and t.get('type') == 'tags']}")
        posts = []
        for i in (d.get('data') if isinstance(d.get('data'), list) else []) + (d.get('included') or []):
            if isinstance(i, dict) and i.get('type') == 'posts':
                posts.append(i)
        users = {u.get('id'): u.get('attributes', {}).get('username') for u in (d.get('included') or []) if isinstance(u, dict) and u.get('type') == 'users'}
        posts.sort(key=lambda p: p.get('attributes', {}).get('number') or 0)
        for p in posts[:5]:
            a = p.get('attributes', {})
            print(f"  #{a.get('number')} {a.get('createdAt','')[:16]} :: {head_text(p)}")
    except Exception as e:
        print(f'[{tid}] parse fail: {e}')
print(f'TS={TS}')
