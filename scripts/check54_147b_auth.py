import json, os

OUT = '/home/z/my-project/output/evidence_post'
TS = '20261022_0430'

def load(f):
    d = json.load(open(os.path.join(OUT, f)))
    users = {u['id']: u['attributes'].get('username') for u in d.get('included', []) if u.get('type') == 'users'}
    raw = d['data'] if isinstance(d['data'], list) else [d['data']]
    posts = [p for p in raw if isinstance(p, dict) and p.get('type') == 'posts']
    posts += [p for p in d.get('included', []) if isinstance(p, dict) and p.get('type') == 'posts']
    disc = d['data'] if isinstance(d['data'], dict) and d['data'].get('type') == 'discussions' else None
    if disc is None:
        for x in d.get('included', []):
            if isinstance(x, dict) and x.get('type') == 'discussions':
                disc = x; break
    return users, posts, disc

# === NEW 196802: OP + metadata ===
users, posts, disc = load(f'discussion_196802_near1_{TS}.json')
if disc:
    a = disc['attributes']
    print(f"NEW 196802: title={a.get('title')!r} createdAt={a.get('createdAt')} cc={a.get('commentCount')} LPN={a.get('lastPostNumber')} locked={a.get('locked')}")
for p in sorted(posts, key=lambda x: x['attributes'].get('number') or 0):
    n = p['attributes'].get('number')
    uid = p['relationships']['user']['data']['id']
    ct = (p['attributes'].get('contentPlain') or '').replace(chr(10), ' ')[:70]
    print(f"  #{n} {p['attributes']['createdAt'][11:16]} {users.get(uid)}: {ct}")

# === авторства дельт ===
print()
targets = {
    '196810': [68, 69, 70], '196778': [44, 45, 46, 47, 48, 49], '196823': [7, 8],
    '196828': [9, 10, 11, 12], '196820': [14, 15, 16, 17], '196799': [68, 69],
    '196822': [7], '196807': [23], '196749': [45, 46], '196801': [14],
    '196808': [7], '196815': [8, 9],
}
for tid, wants in targets.items():
    f = f'discussion_{tid}_near999999_{TS}.json'
    if not os.path.exists(os.path.join(OUT, f)):
        print(f'{tid}: SNAP MISSING'); continue
    users, posts, disc = load(f)
    da = disc['attributes'] if disc else {}
    print(f"[{tid}] cc={da.get('commentCount')} LPN={da.get('lastPostNumber')}")
    for p in sorted(posts, key=lambda x: x['attributes'].get('number') or 0):
        n = p['attributes'].get('number')
        if n in wants:
            uid = p['relationships']['user']['data']['id']
            ct = (p['attributes'].get('contentPlain') or '').replace(chr(10), ' ')[:80]
            print(f"  #{n} {p['attributes']['createdAt'][11:16]} {users.get(uid)}: {ct}")

# === cc-дырки: 196821/196805/196817 (модерация 146-го — растут?) ===
print()
for tid in (196821, 196805, 196817):
    f = f'discussion_{tid}_near999999_{TS}.json'
    users, posts, disc = load(f)
    da = disc['attributes'] if disc else {}
    print(f"[{tid}] cc={da.get('commentCount')} LPN={da.get('lastPostNumber')} (№188: 196821 cc15/LPN16, 196805 cc31/LPN33, 196817 cc27/LPN28)")
