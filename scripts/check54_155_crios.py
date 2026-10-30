# check54_155_crios.py — точная сверка Crios-постов в окне 11:30..12:30 по relationships.user
# (урок 54-137: head_text цитат начинается с имени цитируемого — run1/фаза-2 строки НЕ авторство)
import json, glob, re, datetime

EV = '/home/z/my-project/output/evidence_post'
WINDOW = ('2026-10-22T11:30', '2026-10-22T12:40')

def users_map(d):
    return {u['id']: u['attributes'].get('username','?') for u in d.get('included', [])
            if isinstance(u, dict) and u.get('type')=='users'}

def posts_of(d):
    out = []
    data = d.get('data', [])
    if isinstance(data, dict): data = [data]
    for p in data:
        if isinstance(p, dict) and p.get('type')=='posts': out.append(p)
    for p in d.get('included', []):
        if isinstance(p, dict) and p.get('type')=='posts': out.append(p)
    return out

print('=== ВСЕ посты Crios в снапах 1230 (createdAt 11:30-12:40) ===')
for fn in sorted(glob.glob(f'{EV}/discussion_*_near*_20261022_1230.json')):
    tid = re.search(r'discussion_(\d+)_near', fn)
    if not tid: continue
    tid = tid.group(1)
    try:
        d = json.load(open(fn, encoding='utf-8'))
    except Exception:
        continue
    ums = users_map(d)
    for p in posts_of(d):
        pr = p.get('relationships', {}).get('user', {})
        pu = pr['data']['id'] if pr.get('data') else None
        uname = ums.get(pu, f'user{pu}') if pu else '?'
        ca = p.get('attributes', {}).get('createdAt', '')
        if uname == 'Crios' and WINDOW[0] <= ca <= WINDOW[1]:
            num = p.get('attributes', {}).get('number')
            head = re.sub('<[^>]+>', '', p.get('attributes', {}).get('contentHtml', '') or '')[:70]
            print(f'  d/{tid} #{num} {ca[11:19]} :: {head}')

print()
print('=== GG rx структура #14590 из near14590 снапа ===')
d = json.load(open(f'{EV}/discussion_159759_near14590_20261022_1230.json', encoding='utf-8'))
rels_types = {}
for inc in d.get('included', []):
    if isinstance(inc, dict):
        rels_types[inc.get('type')] = rels_types.get(inc.get('type'), 0) + 1
print('included types:', rels_types)
for p in posts_of(d):
    n = p.get('attributes', {}).get('number')
    if n in (14590, 14591):
        a = p.get('attributes', {})
        print(f"#{n}: likes={a.get('likesCount')} reactionCounts={a.get('reactionCounts', 'N/A')} keys={list(a.keys())[:15]}")
        rr = p.get('relationships', {}).get('reactions', {})
        print(f"   relationships.reactions = {json.dumps(rr)[:300]}")
