#!/usr/bin/env python3
# rescan54_77b_phase2.py — OP-догрузка NEW 196679/196647 + хвосты моверов (Task 54-77)
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

def op_info(tid, tag):
    d = get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json')
    a = d['data']['attributes']
    inc = d.get('included', [])
    users = {i['id']: i['attributes'].get('username', '?') for i in inc if i['type'] == 'users'}
    posts = [i for i in inc if i['type'] == 'posts']
    first = sorted(posts, key=lambda x: x['attributes'].get('number', 0))[0]
    fu = first['relationships'].get('user', {}).get('data', {}).get('id')
    print(f'[{tid}] {tag}: title={a.get("title")!r} createdAt={a.get("createdAt")} cc={a.get("commentCount")} OP=({first["attributes"].get("createdAt")}) {users.get(fu,"?")}')
    print('  OPtext:', repr(first['attributes'].get('content', ''))[:220])

for tid, tag in ((196679, 'NEW ССОП'), (196647, 'NEW дуды-тени')):
    op_info(tid, tag)
d = get(f'{BASE}/api/discussions/196679?page[near]=999999', f'discussion_196679_near999999_{TS}.json')
for tid in (196646, 196661, 196670, 195083, 179952):
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)
print(f'PHASE2 DONE TS={TS}')
