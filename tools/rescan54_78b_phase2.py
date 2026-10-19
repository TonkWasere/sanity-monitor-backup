#!/usr/bin/env python3
# rescan54_78b_phase2.py — OP-догрузка NEW 196678 + хвосты моверов (Task 54-78)
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

d = get(f'{BASE}/api/discussions/196678?page[near]=1', f'discussion_196678_near1_{TS}.json')
a = d['data']['attributes']
inc = d.get('included', [])
users = {i['id']: i['attributes'].get('username', '?') for i in inc if i['type'] == 'users'}
posts = [i for i in inc if i['type'] == 'posts']
first = sorted(posts, key=lambda x: x['attributes'].get('number', 0))[0]
fu = first['relationships'].get('user', {}).get('data', {}).get('id')
print(f'[196678] title={a.get("title")!r} createdAt={a.get("createdAt")} cc={a.get("commentCount")} OP=({first["attributes"].get("createdAt")}) {users.get(fu,"?")}')
for tid in (196678, 196646, 196501, 196666, 196667, 196661, 179952):
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)
print(f'PHASE2 DONE TS={TS}')
