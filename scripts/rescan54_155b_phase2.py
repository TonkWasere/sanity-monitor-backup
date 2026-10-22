import json, os, urllib.request, time, re

TS = '20261022_1230'
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

# ---- 1) NEW d/196840+196841+196842 (три «Дождемся?» за 2 мин): OP near=1 + near999999 (createdAt ВСЕГДА, урок 54-69) ----
for tid in (196840, 196841, 196842):
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

# ---- 1b) GG-якоря #14590/#14591 выпали из near999999 (Санити ожил) — добор near=<номер> (урок 54-135b) ----
print('== GG-якоря добор 159759 near=14590/14591 ==')
gg = {}
for near in (14590, 14591):
    try:
        f = fetch(159759, near, f'GG#{near}')
        d = load(f)
        ums = users_map(d)
        for p in posts_of(d):
            n = p['attributes'].get('number')
            if n in (14590, 14591):
                likes = p['attributes'].get('likesCount', 0)
                rx = {}
                for rel in p.get('relationships', {}).get('reactions', {}).get('data', []) or []:
                    rid = rel.get('id') if isinstance(rel, dict) else None
                    if rid: rx[rid] = rx.get(rid, 0) + 1
                print(f"   #14590 GG {n} likes={likes} rx={rx} :: {re.sub('<[^>]+>', '', p['attributes'].get('contentHtml',''))[:60]}")
                gg[str(n)] = {'likes': likes, 'rx': rx}
    except Exception as e:
        print(f'   GG#{near} FAIL: {e}')
res['gg_anchors'] = gg

# ---- 1c) вне-мониторинговые живые с фронта: 195630 Бан Gex + 195809 Брелок ----
for tid in (195630, 195809):
    print(f'== Контекст d/{tid} near999999 ==')
    try:
        f = fetch(tid, 999999, 'CTX')
        d = load(f)
        ums = users_map(d)
        attrs = d['data']['attributes'] if isinstance(d.get('data'), dict) else {}
        print(f"   [d/{tid}] cc={attrs.get('commentCount')} LPN={attrs.get('lastPostNumber')} locked={attrs.get('locked')}")
        for p in posts_of(d)[-4:]:
            head = re.sub('<[^>]+>', '', p['attributes'].get('contentHtml', ''))[:60]
            print(f"   #{p['attributes'].get('number')} {author_of(p, ums)} {p['attributes'].get('createdAt','?')[11:16]} :: {head}")
    except Exception as e:
        print(f'   CTX FAIL: {e}')

# ---- 2) авторства дельт из снапов 1230 ----
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

print('== Авторства дельт (снапы 1230) ==')
for tid, n in ((196832, 10), (196839, 10), (196838, 6), (196772, 8), (196797, 6), (191614, 6), (196799, 6), (196836, 4), (196837, 4), (196816, 3), (196823, 3), (196814, 3), (112917, 3), (159759, 4)):
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
    res['front_cc_lpn'] = {str(t): ccmap.get(t) for t in (159759, 196832, 196839, 196838, 196837, 196836, 196772, 196797, 196799, 196411, 191614, 196840, 196841, 196842)}
    print('== cc/LPN фронт 1230 ==', res['front_cc_lpn'])

# ---- run1 статистика из лога ----
log = open('/home/z/my-project/scripts/scan54_155_run1.log', encoding='utf-8').read()
ok_n = len(re.findall(r'^OK ', log, re.M))
skip_n = len(re.findall(r'^SKIP ', log, re.M))
fail_n = len(re.findall(r'^FAIL ', log, re.M))
print(f'run1: OK={ok_n} SKIP={skip_n} FAIL={fail_n}')

summary = {
    'task': '54-155', 'ts': TS, 'window': '11:30-12:30 UTC 22.10 (штатный час; 54-154: Арена угасла, NEW 196839 ФЕРМЕР-ВЗРЫВ, 196832 ОФТОП-ВЗРЫВ +17 fast-rule; замер 12:30-12:4x)',
    'run1': {'exit': 0, 'ok': ok_n, 'skip': skip_n, 'fail': fail_n,
             'fail_note': '404-контроли штатные: 196707/196717 (64-й час), 196796 (возврат-контроль 19-й час)',
             'round_streak': '27-Й EXIT=0 ПОДРЯД'},
    'context_note': '54-155: ПОСТ САНЕТИ ОЖИЛ В 23-Й ЧАС (14600->14602, #14601 LordZoHbl 11:53 + #14602 Crios 11:54) — НОЛЬ С 21:21 ПРЕРВАН; CRIOS 3-Й ЧАС АКТИВЕН: #14602 159759 + #24/#26 196839 (шахты/боссы) + #17 196814 + #97 196799 + #36 196772 = 6 ПОСТОВ В 5 ТРЕДАХ; 196832 +34 (52->86, 2-Й middle near=43->69); 196839 +10 (16->26); 196838 АРЕНА ОЖИЛА +4 (12->16: megadonE возврат + Girodjet ×2 + 0Wolk0 в 112917); NEW ×3 «Дождемся?» (196840/196841/196842 12:34-12:36)',
    'new_threads': {f'op_{t}': res.get(f'op_{t}') for t in (196840, 196841, 196842)},
    'gg_anchors_near': res.get('gg_anchors'),
    'authors_deltas': {k: v for k, v in res.items() if k.startswith('authors_')},
    'front_cc_lpn': res.get('front_cc_lpn'),
}
path = f'{EV}/check54_155b_summary.json'
json.dump(summary, open(path, 'w'), ensure_ascii=False, indent=1)
print('OK', path)
