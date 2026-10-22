import json, os, urllib.request, time, re

TS = '20261022_0630'
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
    json.loads(data)
    open(fn, 'wb').write(data)
    print(f'  [GET {tag}] d/{tid} near={near} -> {len(data)}B')
    return fn

def load(fn):
    return json.load(open(fn, encoding='utf-8'))

def users_map(d):
    out = {}
    for u in d.get('included', []):
        if isinstance(u, dict) and u.get('type') == 'users':
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

def author_of(p, ums):
    pr = p.get('relationships', {}).get('user', {})
    pu = pr['data']['id'] if pr.get('data') else None
    return ums.get(pu, f'user{pu}') if pu else '?'

# ---- 1) NEW 196806 ----
print('== 196806 NEW «Что будет на НГ 2026» ==')
f1 = fetch(196806, 1, 'OP')
d1 = load(f1)
dd = d1['data'] if isinstance(d1['data'], dict) else d1['data'][0]
op_attr = dd['attributes']
ums = users_map(d1)
rel = dd.get('relationships', {}).get('user', {})
op_uid = rel['data']['id'] if rel.get('data') else '?'
first_posts = posts_of(d1)
res['new_196806'] = {
    'title': op_attr.get('title'), 'createdAt': op_attr.get('createdAt'),
    'cc': op_attr.get('commentCount'), 'lpn': op_attr.get('lastPostNumber'),
    'lastPostedAt': op_attr.get('lastPostedAt'),
    'op': ums.get(op_uid, f'user{op_uid}') if rel.get('data') else '?',
    'created_before_cutoff_0530': (op_attr.get('createdAt') or '') < '2026-10-22T05:30',
}
res['new_196806']['verdict'] = ('ВСПУХШИЙ ТИХОНЯ (урок 54-136)' if res['new_196806']['created_before_cutoff_0530'] else 'РЕАЛЬНО НОВЫЙ (после 05:30)')
print('  createdAt:', res['new_196806']['createdAt'], '| OP:', res['new_196806']['op'], '| verdict:', res['new_196806']['verdict'])

f2 = fetch(196806, 999999, 'TAIL')
d2 = load(f2)
ums2 = users_map(d2)
tail = []
for p in posts_of(d2)[-10:]:
    tail.append({'num': p['attributes'].get('number'), 'author': author_of(p, ums2),
                 'at': p['attributes'].get('createdAt', '?')[:16],
                 'head': re.sub('<[^>]+>', '', p['attributes'].get('contentHtml', ''))[:60]})
res['new_196806']['tail'] = tail
for t in tail:
    print(f"   #{t['num']} {t['author']} {t['at'][11:16]} :: {t['head'][:48]}")

# ---- 2) 196829 саморазгон: авторства из middle near=19 ----
print('== 196829 middle near=19 авторства ==')
fm = f'{EV}/discussion_196829_near19_20261022_0630.json'
dm = load(fm)
umsm = users_map(dm)
mid = []
for p in posts_of(dm):
    mid.append({'num': p['attributes'].get('number'), 'author': author_of(p, umsm),
                'at': p['attributes'].get('createdAt', '?')[:16],
                'head': re.sub('<[^>]+>', '', p['attributes'].get('contentHtml', ''))[:60]})
mid.sort(key=lambda x: (x['num'] if isinstance(x['num'], int) else 0))
res['authors_196829_middle'] = mid
for t in mid:
    print(f"   #{t['num']} {t['author']} {t['at'][11:16]} :: {t['head'][:48]}")

# хвост 196829 из near999999 0630 (fast-rule скачал)
ft = f'{EV}/discussion_196829_near999999_{TS}.json'
if os.path.exists(ft):
    dt = load(ft)
    umst = users_map(dt)
    tl = [{'num': p['attributes'].get('number'), 'author': author_of(p, umst),
           'at': p['attributes'].get('createdAt', '?')[:16]} for p in posts_of(dt)]
    res['authors_196829_tail'] = tl
    print('   TAIL:'); 
    for t in tl:
        print(f"   #{t['num']} {t['author']} {t['at'][11:16]}")

# ---- 3) авторства остальных дельт из снапов 0630 ----
def tail_authors(tid, n=6):
    fn = f'{EV}/discussion_{tid}_near999999_{TS}.json'
    if not os.path.exists(fn):
        return None
    d = load(fn)
    ums = users_map(d)
    out = []
    for p in posts_of(d)[-n:]:
        head = re.sub('<[^>]+>', '', p['attributes'].get('contentHtml', ''))[:50]
        out.append(f"#{p['attributes'].get('number')} {author_of(p, ums)} {p['attributes'].get('createdAt','?')[11:16]} :: {head}")
    return out

print('== Авторства прочих дельт ==')
for tid, n in ((196820, 4), (196816, 3), (196795, 3), (196828, 3), (196799, 3), (196765, 2)):
    a = tail_authors(tid, n)
    if a:
        print(f'--- d/{tid} ---')
        for x in a:
            print('  ', x)
        res[f'authors_{tid}'] = a

# ---- cc/LPN сверка ----
front_fn = f'{EV}/frontindex_off0_{TS}.json'
if os.path.exists(front_fn):
    fd = load(front_fn)
    ccmap = {int(it['id']): it['attributes'].get('commentCount') for it in fd.get('data', [])}
    res['front_cc'] = {str(t): ccmap.get(t) for t in (196778, 196805, 196806, 196829, 196820, 159759)}
    print('== cc фронт 0630 ==', res['front_cc'])

summary = {
    'task': '54-149', 'ts': TS, 'window': '05:30-06:30 UTC 22.10 (замер 06:28-06:45)',
    'run1': {'exit': 0, 'ok': 234, 'fail': 3,
             'fail_note': '404-контроли штатные: 196796 (14-й час), 196707/196717 (58-й час)',
             'round_streak': '22-Й EXIT=0 ПОДРЯД'},
    'new_196806': res.get('new_196806'),
    'authors_196829_middle': res.get('authors_196829_middle'),
    'authors_196829_tail': res.get('authors_196829_tail'),
    'authors_other': {k: v for k, v in res.items() if k.startswith('authors_') and '196829' not in k},
    'front_cc': res.get('front_cc'),
}
path = f'{EV}/check54_149b_summary.json'
json.dump(summary, open(path, 'w'), ensure_ascii=False, indent=1)
print('OK', path)
