#!/usr/bin/env python3
# rescan54_82b_phase2.py — NEW 196651 near=1 (OP+createdAt+cc проверка, Task 54-82)
import json, os, urllib.request, time, datetime
TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'

def get(url, name):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}'); return json.load(open(path, encoding='utf-8'))
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    d = json.loads(raw.decode('utf-8'))
    open(path, 'wb').write(raw)
    print(f'OK {name} ({len(raw)}B)'); time.sleep(1)
    return d

def dump(tid, d):
    a = d['data']['attributes']
    inc = d.get('included', [])
    users = {i['id']: i['attributes'].get('username', '?') for i in inc if i['type'] == 'users'}
    posts = [i for i in inc if i['type'] == 'posts']
    if not posts:
        print(f'[{tid}] cc={a.get("commentCount")} (no posts in page)'); return
    first = sorted(posts, key=lambda x: x['attributes'].get('number', 0))[0]
    fu = first['relationships'].get('user', {}).get('data', {}).get('id')
    print(f'[{tid}] title={a.get("title")!r} createdAt={a.get("createdAt")} cc={a.get("commentCount")} OP=({first["attributes"].get("createdAt")}) {users.get(fu,"?")}')
    for p in posts[-8:]:
        pa = p['attributes']
        pu = p['relationships'].get('user', {}).get('data', {}).get('id')
        print(f'  #{pa.get("number")} {pa.get("createdAt","?")[:19]} :: {users.get(pu,"?")} {(pa.get("content") or "")[:110]}')

# NEW-проверка: 196651 — near=1 (OP + createdAt; урок 54-69: сверять до «NEW» в ledger)
d = get(f'{BASE}/api/discussions/196651?page[near]=1', f'discussion_196651_near1_{TS}.json')
dump(196651, d)
print(f'PHASE2 DONE TS={TS}')
