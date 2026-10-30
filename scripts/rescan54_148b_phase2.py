import json, os, urllib.request, time, re

TS = '20261022_0530'
EV = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
BASE = 'https://forum.exbo.net/api/discussions/'
res = {}

def fetch(tid, near, tag):
    fn = f'{EV}/discussion_{tid}_{"near1" if near==1 else "near999999"}_{TS}.json'
    if os.path.exists(fn):
        return fn
    url = f'{BASE}{tid}?page%5Bnear%5D={near}' + ('&page%5Blimit%5D=1' if near == 1 else '')
    req = urllib.request.Request(url, headers=UA)
    time.sleep(1)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    json.loads(data)  # validate
    open(fn, 'wb').write(data)
    print(f'  [GET {tag}] d/{tid} near={near} -> {len(data)}B')
    return fn

def load(fn):
    return json.load(open(fn, encoding='utf-8'))

def users_map(d):
    out = {}
    for u in d.get('included', []):
        if u.get('type') == 'users':
            out[u['id']] = u['attributes'].get('username', '?')
    return out

def posts_of(d):
    posts = []
    data = d.get('data', [])
    if isinstance(data, dict):
        data = [data]
    for p in data:
        if isinstance(p, dict) and p.get('type') == 'posts':
            posts.append(p)
    for p in d.get('included', []):
        if isinstance(p, dict) and p.get('type') == 'posts':
            posts.append(p)
    return posts

# ---- 1) NEW 196829: OP + хвост ----
print('== 196829 NEW «День сурка (опять рейтинг)» ==')
f1 = fetch(196829, 1, 'OP')
d1 = load(f1)
op_attr = d1['data']['attributes']
ums = users_map(d1)
rel = d1['data'].get('relationships', {}).get('user', {})
op_uid = rel['data']['id'] if rel.get('data') else '?'
op_name = ums.get(op_uid, f'user{op_uid}')
created = op_attr.get('createdAt', '?')
first_posts = posts_of(d1)
res['new_196829'] = {
    'title': op_attr.get('title'),
    'createdAt': created,
    'cc': op_attr.get('commentCount'),
    'lpn': op_attr.get('lastPostNumber'),
    'lastPostedAt': op_attr.get('lastPostedAt'),
    'op': op_name,
    'first_post_at': first_posts[0]['attributes'].get('createdAt') if first_posts else '?',
    'first_post_author': None,
}
if first_posts:
    pr = first_posts[0].get('relationships', {}).get('user', {})
    pu = pr['data']['id'] if pr.get('data') else None
    res['new_196829']['first_post_author'] = ums.get(pu, f'user{pu}') if pu else '?'
cutoff = '2026-10-22T04:30'
res['new_196829']['created_before_cutoff'] = created < cutoff
res['new_196829']['verdict_note'] = ('ВСПУХШИЙ ТИХОНЯ (урок 54-136)' if created < cutoff else 'РЕАЛЬНО НОВЫЙ (после 04:30)')

f2 = fetch(196829, 999999, 'TAIL')
d2 = load(f2)
ums2 = users_map(d2)
tail = []
for p in posts_of(d2)[-12:]:
    pr = p.get('relationships', {}).get('user', {})
    pu = pr['data']['id'] if pr.get('data') else None
    tail.append({'num': p['attributes'].get('number'), 'author': ums2.get(pu, f'user{pu}') if pu else '?',
                 'at': p['attributes'].get('createdAt', '?')[:16],
                 'head': re.sub('<[^>]+>', '', p['attributes'].get('contentHtml', ''))[:70]})
res['new_196829']['tail'] = tail

# ---- 2) Авторства дельт из снапов 0530 (без GET) ----
def tail_authors(tid, n=8):
    fn = f'{EV}/discussion_{tid}_near999999_{TS}.json'
    if not os.path.exists(fn):
        return None
    d = load(fn)
    ums = users_map(d)
    out = []
    for p in posts_of(d)[-n:]:
        pr = p.get('relationships', {}).get('user', {})
        pu = pr['data']['id'] if pr.get('data') else None
        head = re.sub('<[^>]+>', '', p['attributes'].get('contentHtml', ''))[:55]
        out.append(f"#{p['attributes'].get('number')} {ums.get(pu,'?')} {p['attributes'].get('createdAt','?')[11:16]} :: {head}")
    return out

print('== Авторства дельт (из снапов 0530) ==')
for tid, n in ((196820, 12), (196810, 6), (196778, 8), (196814, 4), (196799, 4), (196755, 3), (196828, 4), (196802, 6)):
    a = tail_authors(tid, n)
    if a:
        print(f'--- d/{tid} ---')
        for x in a:
            print('  ', x)
        res[f'authors_{tid}'] = a

# ---- 3) cc vs LPN (дырки/удаления) по снапам 0530 + фронт ----
front_fn = f'{EV}/frontindex_off0_{TS}.json'
if os.path.exists(front_fn):
    fd = load(front_fn)
    ccmap = {}
    for it in fd.get('data', []):
        ccmap[int(it['id'])] = it['attributes'].get('commentCount')
    res['front_cc'] = {str(t): ccmap.get(t) for t in (196821, 196805, 196817, 196823, 196778, 196802, 196820, 196829, 159759)}
    print('== cc (фронт 0530) ==', res['front_cc'])

# ---- 4) Талоны 196452 (флешмоб) + Схрон-линия ----
fn452 = f'{EV}/discussion_196452_near999999_{TS}.json'
if os.path.exists(fn452):
    d = load(fn452)
    res['talony_196452'] = {'cc': d['data']['attributes'].get('commentCount'), 'lpn': d['data']['attributes'].get('lastPostNumber')}

# ---- summary ----
summary = {
    'task': '54-148', 'ts': TS, 'window': '04:30-05:30 UTC 22.10 (замер 05:28-05:45)',
    'run1': {'exit': 0, 'ok': 233, 'fail': 3,
             'fail_note': '404-контроли штатные: 196796 (13-й час), 196707/196717 (57-й час)',
             'round_streak': '21-Й EXIT=0 ПОДРЯД'},
    'new_196829': res.get('new_196829'),
    'authors': {k: v for k, v in res.items() if k.startswith('authors_')},
    'front_cc': res.get('front_cc'),
    'talony_196452': res.get('talony_196452'),
}
path = f'{EV}/check54_148b_summary.json'
json.dump(summary, open(path, 'w'), ensure_ascii=False, indent=1)
print('OK', path)
