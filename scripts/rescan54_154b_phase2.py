import json, os, urllib.request, time, re

TS = '20261022_1130'
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

# ---- 1) NEW d/196839: OP near=1 + near999999 (createdAt ВСЕГДА, урок 54-69) ----
for tid in (196839,):
    print(f'== NEW d/{tid}: OP near=1 + near999999 ==')
    try:
        fo = fetch(tid, 1, 'OP')
        do = load(fo)
        umso = users_map(do)
        po = posts_of(do)
        if po:
            p0 = po[0]
            print(f"   OP #{p0['attributes'].get('number')} {author_of(p0, umso)} {p0['attributes'].get('createdAt','?')[:19]} :: {re.sub('<[^>]+>', '', p0['attributes'].get('contentHtml',''))[:90]}")
            res[f'op_{tid}'] = {'author': author_of(p0, umso), 'createdAt': p0['attributes'].get('createdAt'), 'head': re.sub('<[^>]+>', '', p0['attributes'].get('contentHtml',''))[:200]}
    except Exception as e:
        print(f'   OP FAIL: {e}')
    try:
        fe = fetch(tid, 999999, 'TAIL')
        de = load(fe)
        umse = users_map(de)
        tl = []
        for p in posts_of(de)[-8:]:
            head = re.sub('<[^>]+>', '', p['attributes'].get('contentHtml', ''))[:50]
            tl.append(f"#{p['attributes'].get('number')} {author_of(p, umse)} {p['attributes'].get('createdAt','?')[11:16]} :: {head}")
        res[f'tail_{tid}'] = tl
        for x in tl:
            print('  ', x)
    except Exception as e:
        print(f'   TAIL FAIL: {e}')

# ---- 2) авторства дельт из снапов 1030 ----
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

print('== Авторства дельт (снапы 1130) ==')
for tid, n in ((196832, 8), (196799, 10), (196839, 8), (196838, 3), (196837, 6), (196836, 4), (196814, 4), (196770, 4), (196795, 3), (196805, 2), (196772, 2), (196784, 2), (196806, 4), (191614, 4), (196829, 3), (112917, 2)):
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
    res['front_cc_lpn'] = {str(t): ccmap.get(t) for t in (159759, 196806, 196829, 196832, 196830, 196799, 196411, 196837, 196838, 196839, 196836)}
    print('== cc/LPN фронт 1030 ==', res['front_cc_lpn'])

# ---- run1 статистика из лога ----
log = open('/home/z/my-project/scripts/scan54_154_run1.log', encoding='utf-8').read()
ok_n = len(re.findall(r'^OK ', log, re.M))
skip_n = len(re.findall(r'^SKIP ', log, re.M))
fail_n = len(re.findall(r'^FAIL ', log, re.M))
print(f'run1: OK={ok_n} SKIP={skip_n} FAIL={fail_n}')

summary = {
    'task': '54-154', 'ts': TS, 'window': '10:30-11:30 UTC 22.10 (штатный час; после 54-153b — АРЕНА МИТРОПОЛИТА 196838 + TG 3225 11:00; замер 11:30-11:4x)',
    'run1': {'exit': 0, 'ok': ok_n, 'skip': skip_n, 'fail': fail_n,
             'fail_note': '404-контроли штатные: 196707/196717 (63-й час), 196796 (возврат-контроль 18-й час)',
             'round_streak': '26-Й EXIT=0 ПОДРЯД'},
    'context_note': '54-153b: АРЕНА МИТРОПОЛИТА — 196838 (OP Girodjet 10:27:39, ОФФ ожил) + TG stalzone 3225 11:00:21 (❤148); WIPE-9-зеркало второй ВМ закрыто (ff-merge + vault sha256 = эталон); 196839 NEW-взрыв cc 1->11',
    'new_threads': {'op_196839': res.get('op_196839'), 'tail_196839': res.get('tail_196839')},
    'authors_deltas': {k: v for k, v in res.items() if k.startswith('authors_')},
    'front_cc_lpn': res.get('front_cc_lpn'),
}
path = f'{EV}/check54_154b_summary.json'
json.dump(summary, open(path, 'w'), ensure_ascii=False, indent=1)
print('OK', path)
