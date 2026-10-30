import json, os, urllib.request, time, re

TS = '20261022_0830'
EV = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
BASE = 'https://forum.exbo.net/api/discussions/'
res = {}

def fetch(tid, near, tag):
    fn = f'{EV}/discussion_{tid}_near{near}_{TS}.json'
    if os.path.exists(fn):
        return fn
    url = f'{BASE}{tid}?page%5Bnear%5D={near}'
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

# ---- 1) 196806 middle near=39 (вспухший тихоня +16 за гэп: 31->47) ----
print('== 196806 middle near=39 (гэп-вспух: 31->47) ==')
fm = fetch(196806, 39, 'MIDDLE')
dm = load(fm)
umsm = users_map(dm)
mid = []
for p in posts_of(dm):
    head = re.sub('<[^>]+>', '', p['attributes'].get('contentHtml', ''))[:55]
    mid.append({'num': p['attributes'].get('number'), 'author': author_of(p, umsm),
                'at': p['attributes'].get('createdAt', '?')[:16], 'head': head})
mid.sort(key=lambda x: (x['num'] if isinstance(x['num'], int) else 0))
res['authors_196806_middle'] = mid
for t in mid:
    print(f"   #{t['num']} {t['author']} {t['at'][11:16]} :: {t['head'][:48]}")

# tail 196806 из снапа 0830 (fast-rule скачал near999999)
ft = f'{EV}/discussion_196806_near999999_{TS}.json'
if os.path.exists(ft):
    dt = load(ft)
    umst = users_map(dt)
    tl = []
    for p in posts_of(dt)[-8:]:
        head = re.sub('<[^>]+>', '', p['attributes'].get('contentHtml', ''))[:50]
        tl.append(f"#{p['attributes'].get('number')} {author_of(p, umst)} {p['attributes'].get('createdAt','?')[11:16]} :: {head}")
    res['tail_196806'] = tl
    print('   TAIL 0830:')
    for x in tl:
        print('  ', x)

# ---- 2) авторства прочих дельт из снапов 0830 (гэп: 2 часа нарезки) ----
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

print('== Авторства прочих дельт (снапы 0830) ==')
for tid, n in ((196829, 6), (196820, 4), (196819, 5), (196816, 4), (196778, 4), (196828, 3), (196823, 3), (196799, 2), (196749, 2), (196802, 2), (196827, 2), (196812, 2)):
    a = tail_authors(tid, n)
    if a:
        print(f'--- d/{tid} ---')
        for x in a:
            print('  ', x)
        res[f'authors_{tid}'] = a

# ---- cc/LPN сверка по фронту ----
front_fn = f'{EV}/frontindex_off0_{TS}.json'
if os.path.exists(front_fn):
    fd = load(front_fn)
    ccmap = {int(it['id']): (it['attributes'].get('commentCount'), it['attributes'].get('lastPostNumber')) for it in fd.get('data', [])}
    res['front_cc_lpn'] = {str(t): ccmap.get(t) for t in (159759, 196778, 196805, 196806, 196829, 196820, 196411)}
    print('== cc/LPN фронт 0830 ==', res['front_cc_lpn'])

# ---- run1 статистика из лога ----
log = open('/home/z/my-project/scripts/scan54_151_run1.log', encoding='utf-8').read()
ok_n = len(re.findall(r'^OK ', log, re.M))
skip_n = len(re.findall(r'^SKIP ', log, re.M))
fail_n = len(re.findall(r'^FAIL ', log, re.M))
print(f'run1: OK={ok_n} SKIP={skip_n} FAIL={fail_n}')

summary = {
    'task': '54-151', 'ts': TS, 'window': '06:30-08:30 UTC 22.10 (ГЭП 1 ч — 54-150 cron-сессия оборвалась; замер 08:28-08:4x)',
    'run1': {'exit': 0, 'ok': ok_n, 'skip': skip_n, 'fail': fail_n,
             'fail_note': '404-контроли штатные: 196796 (15-й час), 196707/196717 (59-60-й час)',
             'round_streak': '23-Й EXIT=0 ПОДРЯД'},
    'gap_note': '54-150 не выполнялся: дельты 06:30..08:30 одним обходом',
    'authors_196806_middle': res.get('authors_196806_middle'),
    'tail_196806': res.get('tail_196806'),
    'authors_other': {k: v for k, v in res.items() if k.startswith('authors_') and '196806' not in k},
    'front_cc_lpn': res.get('front_cc_lpn'),
}
path = f'{EV}/check54_151b_summary.json'
json.dump(summary, open(path, 'w'), ensure_ascii=False, indent=1)
print('OK', path)
