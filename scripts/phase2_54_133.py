# -*- coding: utf-8 -*-
# phase2_54_133.py — OP near=1 для NEW 196803/196804 (БЕЗ include — урок 54-131)
import json, os, urllib.request, time, datetime, re

TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
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
        print(f'OK {name} ({len(body)}B)')
        return True
    except Exception as e:
        print(f'FAIL {name}: {e}')
        return False

def head(p, n=200):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or a.get('contentHtml') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()[:n]

for tid in (196803, 196804):
    fn = f'discussion_{tid}_near1_{TS}.json'
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', fn)
    time.sleep(1)
    try:
        d = json.load(open(os.path.join(OUT, fn)))
    except Exception as e:
        print(f'[{tid}] parse fail {e}'); continue
    a = d.get('data', {}).get('attributes', {})
    rel = d.get('data', {}).get('relationships', {})
    tags = [(rel.get('tags', {}).get('data') or [])]
    tagids = [t['id'] for t in (rel.get('tags', {}).get('data') or [])]
    groups = {i['id']: (i.get('attributes', {}) or {}).get('nameSingular')
              for i in (d.get('included') or []) if i.get('type') == 'groups'}
    users = {i['id']: i for i in (d.get('included') or []) if i.get('type') == 'users'}
    print(f"\n=== [{tid}] «{a.get('title')}» createdAt={a.get('createdAt')} cc={a.get('commentCount')} "
          f"LPN={a.get('lastPostNumber')} locked={a.get('isLocked')} sticky={a.get('sticky')} tags={tagids}")
    opid = ((rel.get('user', {}) or {}).get('data', {}) or {}).get('id')
    u = users.get(opid) or {}
    ua = u.get('attributes', {})
    gids = [x.get('id') for x in (u.get('relationships', {}) or {}).get('groups', {}).get('data', [])]
    print(f"  OP={ua.get('username')} groups={[groups.get(g, g) for g in gids]} "
          f"join={(ua.get('joinTime') or '?')[:10]} cc={ua.get('commentCount')} "
          f"discussions={ua.get('discussionCount')}")
    posts = [i for i in (d.get('included') or []) if i.get('type') == 'posts']
    for p in sorted(posts, key=lambda x: x.get('attributes', {}).get('number') or 0)[:3]:
        pa = p.get('attributes', {})
        pid = (p.get('relationships', {}).get('user', {}) or {}).get('data', {}).get('id')
        pu = users.get(pid, {}).get('attributes', {})
        print(f"  #{pa.get('number')} [{pa.get('createdAt')}] {pu.get('username','?')} :: {head(p)}")
print(f'\nTS={TS}')
