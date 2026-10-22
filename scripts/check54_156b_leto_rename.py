import json, glob, re

def norm(d):
    out = []
    for src in ('data', 'included'):
        v = d.get(src, [])
        if isinstance(v, dict):
            v = [v]
        out += [x for x in v if isinstance(x, dict) and x.get('type') == 'posts']
    return out

# 1) historical authorship of #14590..14593 + search LetoArbaletov in users
for fn in sorted(glob.glob('output/evidence_post/discussion_159759_near999999_2026102*.json'))[-8:]:
    dd = json.load(open(fn, encoding='utf-8'))
    uu = {u['id']: u['attributes'].get('username', '?') for u in dd.get('included', []) if isinstance(u, dict) and u.get('type') == 'users'}
    ts = fn.split('_')[-1].replace('.json', '')
    for pp in norm(dd):
        num = pp['attributes'].get('number')
        if num in (14590, 14591, 14592, 14593):
            ud = pp.get('relationships', {}).get('user', {}).get('data', {})
            print(f'{ts} #{num} id={pp["id"]} author={uu.get(ud.get("id"), "?")}(uid={ud.get("id")})')
    for u in dd.get('included', []):
        if isinstance(u, dict) and u.get('type') == 'users' and 'eto' in u['attributes'].get('username', '').lower():
            print(f'{ts} USER IN SNAPSHOT: {u["attributes"].get("username")} uid={u["id"]}')

print()
# 2) anchor 14591 author from latest phase-2 fetch
fs = sorted(glob.glob('output/evidence_post/discussion_159759_near14591_20261022_13*.json'))
fn = fs[-1]
dd = json.load(open(fn, encoding='utf-8'))
uu = {u['id']: u['attributes'].get('username', '?') for u in dd.get('included', []) if isinstance(u, dict) and u.get('type') == 'users'}
for pp in norm(dd):
    if pp['attributes'].get('number') == 14591:
        ud = pp.get('relationships', {}).get('user', {}).get('data', {})
        ts = fn.split('_')[-1]
        print(f'ANCHOR #14591 [{ts}]: author={uu.get(ud.get("id"), "?")}(uid={ud.get("id")}) at {pp["attributes"].get("createdAt", "")[:19]}')
        rx = {k: v for k, v in pp['attributes'].get('reactionCounts', {}).items() if v}
        print(f'   likes={pp["attributes"].get("likesCount")} rx_nonzero={rx}')

# 3) scan ALL snapshot users across all days for PatronOfSanity / LetoArbaletov uid presence
print()
seen = {}
for fn in glob.glob('output/evidence_post/discussion_159759_*.json'):
    try:
        dd = json.load(open(fn, encoding='utf-8'))
    except Exception:
        continue
    for u in dd.get('included', []):
        if isinstance(u, dict) and u.get('type') == 'users':
            nm = u['attributes'].get('username', '?')
            if nm in ('PatronOfSanity', 'LetoArbaletov', 'GetGood', 'Virusnyaga'):
                key = (nm, u['id'])
                seen[key] = seen.get(key, 0) + 1
print('user presence across ALL 159759 snapshots:')
for (nm, uid), cnt in sorted(seen.items()):
    print(f'  {nm} uid={uid}: in {cnt} snapshots')
