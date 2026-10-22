import json, os, urllib.request, time, re

TS = '20261022_1330'
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

# ---- 1) NEW d/196844 (Тима для нового рейтинга, cc=21 на 13:35 — взрывной старт) + d/196846 (Пятерочки): OP near=1 + near999999 ----
for tid in (196844, 196846):
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

# ---- 1b) проверка сноса 196840/196841 (OP сам просил; run1 404) — официальная фиксация ----
for tid in (196840, 196841):
    print(f'== СНОС-ЧЕК d/{tid} OP near=1 ==')
    try:
        fo = fetch(tid, 1, 'WIPE-CHECK')
        do = load(fo)
        po = posts_of(do)
        if po:
            print(f'   ВСЁ ЕЩЁ ЖИВ: OP #{po[0]["attributes"].get("number")} createdAt={po[0]["attributes"].get("createdAt")}')
    except Exception as e:
        print(f'   ПОДТВЕРЖДЁН 404 = СНЕСЕН: {e}')
        res[f'wiped_{tid}'] = True

# ---- 1c) GG-якоря #14590/#14591 (снова выпали из near999999) — добор near=<номер> ----
print('== GG-якоря добор 159759 near=14590/14591 ==')
gg = {}
for near in (14590, 14591):
    try:
        f = fetch(159759, near, f'GG#{near}')
        d = load(f)
        for p in posts_of(d):
            n = p['attributes'].get('number')
            if n in (14590, 14591):
                likes = p['attributes'].get('likesCount', 0)
                rc = {k: v for k, v in (p['attributes'].get('reactionCounts') or {}).items() if v}
                print(f"   GG #{n} likes={likes} rx={rc}")
                gg[str(n)] = {'likes': likes, 'rx': rc}
    except Exception as e:
        print(f'   GG#{near} FAIL: {e}')
res['gg_anchors'] = gg

# ---- 1d) Санити-авторства #14601/#14602 по relationships.user (урок 54-137; ledger №196 vs summary противоречие) ----
print('== Санити 159759 #14601/#14602 АВТОРСТВА (relationships.user) ==')
try:
    f = fetch(159759, 14601, 'SANITY-AUTH')
    d = load(f)
    ums = users_map(d)
    for p in posts_of(d):
        n = p['attributes'].get('number')
        if n in (14601, 14602):
            print(f"   #{n} автор={author_of(p, ums)} {p['attributes'].get('createdAt','?')[11:19]} :: {re.sub('<[^>]+>', '', p['attributes'].get('contentHtml',''))[:70]}")
            res[f'sanity_{n}'] = {'author': author_of(p, ums), 'createdAt': p['attributes'].get('createdAt')}
except Exception as e:
    print(f'   SANITY-AUTH FAIL: {e}')

# ---- 2) авторства дельт из снапов 1330 ----
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

print('== Авторства дельт (снапы 1330) ==')
for tid, n in ((196838, 8), (196842, 8), (196832, 10), (196836, 6), (196819, 6), (196799, 6), (196828, 4), (112917, 4), (196844, 8), (196846, 4)):
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
    res['front_cc_lpn'] = {str(t): ccmap.get(t) for t in (159759, 196832, 196839, 196838, 196837, 196836, 196772, 196797, 196799, 196411, 191614, 196842, 196844, 196846, 196828, 196819)}
    print('== cc/LPN фронт 1330 ==', res['front_cc_lpn'])

# ---- run1 статистика из лога ----
log = open('/home/z/my-project/scripts/scan54_156_run1.log', encoding='utf-8').read()
ok_n = len(re.findall(r'^OK ', log, re.M))
skip_n = len(re.findall(r'^SKIP ', log, re.M))
fail_n = len(re.findall(r'^FAIL ', log, re.M))
print(f'run1: OK={ok_n} SKIP={skip_n} FAIL={fail_n}')

summary = {
    'task': '54-156', 'ts': TS, 'window': '12:30-13:30 UTC 22.10 (штатный час; 54-155: Санити ОЖИЛ Crios #14601, Crios 3-й час 5 постов/4 треда, 196832 +34, NEW x3 трипл-дубль, Арена ОЖИЛА megadonE; замер 13:30-13:4x)',
    'run1': {'exit': 0, 'ok': ok_n, 'skip': skip_n, 'fail': fail_n,
             'fail_note': '196840/196841 HTTP 404 = СНЕСЕНЫ (OP сам просил, трипл-дубль 12:31/12:32; 196842 ЖИВ) + 404-контроли 196707/196717 (65-й час) + 196796 (возврат 20-й час)',
             'round_streak': '28-Й EXIT=0 ПОДРЯД'},
    'context_note': '54-156: ★ 196840/196841 СНЕСЕНЫ за час (модерация сработала на OP-просьбу; 196842 живёт органикой 25->30 ткб-408-спор); ★ АРЕНА 196838 3-Й ЧАС РОСТА 16->22 (+6, cc=20); ★ 196832 ЗАМЕДЛИЛСЯ 86->94 (+8, 3-й middle не нужен); Жига 196836 10->15 (+5); NEW ×2 = 196844 «Тима для нового рейтинга» (13:34, cc=21 взрывной старт) + 196846 «Пятерочки тред» (13:34, cc=1); 196819 +5 (14->19); Санити 24-Й ЧАС = рест (14602 стоит); ТГК 3225 последний',
    'new_threads': {f'op_{t}': res.get(f'op_{t}') for t in (196844, 196846)},
    'wiped': {t: res.get(f'wiped_{t}', False) for t in (196840, 196841)},
    'gg_anchors_near': res.get('gg_anchors'),
    'sanity_authorship': {k: res.get(k) for k in ('sanity_14601', 'sanity_14602')},
    'authors_deltas': {k: v for k, v in res.items() if k.startswith('authors_')},
    'front_cc_lpn': res.get('front_cc_lpn'),
}
path = f'{EV}/check54_156b_summary.json'
json.dump(summary, open(path, 'w'), ensure_ascii=False, indent=1)
print('OK', path)
