import json, os, urllib.request, time, re

TS = '20261022_1530'
EV = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
BASE = 'https://forum.exbo.net/api/discussions/'
res = {}

def fetch(tid, near, tag, extra=''):
    fn = f'{EV}/discussion_{tid}_near{near}_{TS}.json'
    if os.path.exists(fn):
        print(f'  SKIP d/{tid} near={near}'); return fn
    url = f'{BASE}{tid}?page%5Bnear%5D={near}{extra}'
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
    return {u['id']: u['attributes'].get('username', '?')
            for u in d.get('included', []) if isinstance(u, dict) and u.get('type') == 'users'}

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

def plain(html):
    t = re.sub(r'<blockquote.*?</blockquote>', ' [Q] ', html or '', flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

# ---- 0) NEW x5: 196856 / 196857 / 196860 / 196861 / 196843 — OP near=1 + near999999 ----
for tid in (196856, 196857, 196860, 196861, 196843):
    print(f'== NEW d/{tid}: OP near=1 + near999999 ==')
    try:
        fo = fetch(tid, 1, 'OP')
    except Exception as e:
        print(f'  OP FAIL d/{tid}: {e}'); continue
    do = load(fo)
    ums = users_map(do)
    po = sorted(posts_of(do), key=lambda p: p['attributes'].get('number', 0))
    if po:
        p0 = po[0]
        a0 = p0['attributes']
        ud = p0.get('relationships', {}).get('user', {}).get('data', {})
        dd = do.get('data', {}).get('attributes', {}) if isinstance(do.get('data'), dict) else {}
        print(f"  OP #{a0.get('number')} [{a0.get('createdAt')}] {ums.get(ud.get('id'),'?')}(uid={ud.get('id')}) cc={dd.get('commentCount','?')} title={dd.get('title','?')}")
        print(f"  OP text: {plain(a0.get('contentHtml',''))[:260]}")
        for p in po[1:4]:
            a = p['attributes']
            print(f"    #{a.get('number')} [{a.get('createdAt','')[11:16]}] {author_of(p, ums)}: {plain(a.get('contentHtml',''))[:100]}")
    try:
        ft = fetch(tid, 999999, 'TAIL')
    except Exception as e:
        print(f'  TAIL FAIL d/{tid}: {e}'); continue
    dt = load(ft)
    umst = users_map(dt)
    pt = sorted(posts_of(dt), key=lambda p: p['attributes'].get('number', 0))
    print(f'  TAIL: {len(pt)} posts, номера {[p["attributes"].get("number") for p in pt]}')
    for p in pt[-6:]:
        a = p['attributes']
        print(f"    #{a.get('number')} [{a.get('createdAt','')[11:16]}] {author_of(p, umst)}: {plain(a.get('contentHtml',''))[:100]}")

# ---- 1) Санити: near=14607 (страница 14601-14609: новые >=14606 + авторства rel.user) ----
print('== САНИТИ 159759 near=14607: посты 26-Й ЧАС + авторства (incl. #14606 «Crios» в head_text) ==')
fs = fetch(159759, 14607, 'SANITI-NEW')
d = load(fs)
ums = users_map(d)
po = sorted(posts_of(d), key=lambda p: p['attributes'].get('number', 0))
print(f'  страница: {[p["attributes"].get("number") for p in po]}')
for p in po:
    if p['attributes'].get('number', 0) >= 14606:
        a = p['attributes']
        ud = p.get('relationships', {}).get('user', {}).get('data', {})
        print(f"  #{a.get('number')} [{a.get('createdAt')}] {ums.get(ud.get('id'),'?')}(uid={ud.get('id')})")
        print(f"     text: {plain(a.get('contentHtml',''))[:240]}")

# ---- 2) GG-якоря: near=14590 (страница 14581-14600 => #14590+#14591 одним снапом) ----
print('== GG-ЯКОРЯ near=14590 ==')
fg = fetch(159759, 14590, 'GG')
dg = load(fg)
umg = users_map(dg)
for p in posts_of(dg):
    n = p['attributes'].get('number')
    if n in (14590, 14591):
        rx = {k: v for k, v in p['attributes'].get('reactionCounts', {}).items() if v}
        likes = [umg.get(l['id'], l['id']) for l in p.get('relationships', {}).get('likes', {}).get('data', [])]
        print(f'  #{n}: likes={p["attributes"].get("likesCount")} liked_by={likes} rx_nonzero={rx}')

# ---- 3) cc-контроль чисток: 196752 (cc 24?) + 196778 (cc 52?) — дыры в видимых номерах ----
print('== 196752 Слухи: чистка продолжилась? видимые номера (LPN=28, cc=24) ==')
f752 = f'{EV}/discussion_196752_near999999_{TS}.json'
if os.path.exists(f752):
    d752 = load(f752)
    nums = sorted(p['attributes'].get('number') for p in posts_of(d752) if isinstance(p.get('attributes'), dict))
    print(f'  видимый хвост: {nums}')
else:
    print('  (снапа нет — SKIP в run1?)')
print('== 196778 Цепь Распада: видимые номера (LPN=54, cc=52) ==')
f778 = f'{EV}/discussion_196778_near999999_{TS}.json'
if os.path.exists(f778):
    d778 = load(f778)
    ums778 = users_map(d778)
    nums = sorted(p['attributes'].get('number') for p in posts_of(d778) if isinstance(p.get('attributes'), dict))
    print(f'  видимый хвост: {nums}')
    for p in posts_of(d778):
        if p['attributes'].get('number', 0) >= 50:
            a = p['attributes']
            print(f"  #{a.get('number')} [{a.get('createdAt','')[5:16]}] {author_of(p, ums778)}: {plain(a.get('contentHtml',''))[:110]}")
else:
    print('  (снапа нет — SKIP в run1?)')

# ---- 4) 196854 вспышка: кто пишет хвост (флейм kravv285? мод?) ----
print('== 196854 (LPN 38, вспышка): авторы хвоста ==')
f854 = f'{EV}/discussion_196854_near999999_{TS}.json'
if os.path.exists(f854):
    d854 = load(f854)
    ums854 = users_map(d854)
    for p in sorted(posts_of(d854), key=lambda x: x['attributes'].get('number', 0)):
        n = p['attributes'].get('number', 0)
        if n >= 30:
            a = p['attributes']
            print(f"  #{n} [{a.get('createdAt','')[11:16]}] {author_of(p, ums854)}: {plain(a.get('contentHtml',''))[:110]}")
else:
    print('  (снапа нет)')

# ---- 5) 196799 спор: Crios 3-й пост? (хвост >=113) ----
print('== 196799 (LPN 112+): авторы хвоста ==')
f799 = f'{EV}/discussion_196799_near999999_{TS}.json'
if os.path.exists(f799):
    d799 = load(f799)
    ums799 = users_map(d799)
    for p in sorted(posts_of(d799), key=lambda x: x['attributes'].get('number', 0)):
        n = p['attributes'].get('number', 0)
        if n >= 113:
            a = p['attributes']
            print(f"  #{n} [{a.get('createdAt','')[11:16]}] {author_of(p, ums799)}: {plain(a.get('contentHtml',''))[:110]}")
else:
    print('  (снапа нет)')

# ---- 6) хвосты-авторы: 196846 (>=27), 196844 (>=32), 196851 (>=8), 196853 (>=15), 196838 (>=24) ----
for tid, frm in ((196846, 27), (196844, 32), (196851, 8), (196853, 15), (196838, 24)):
    fnx = f'{EV}/discussion_{tid}_near999999_{TS}.json'
    if not os.path.exists(fnx):
        print(f'== d/{tid}: (снапа нет) =='); continue
    print(f'== d/{tid}: авторы хвоста (>=#{frm}) ==')
    dx = load(fnx)
    umx = users_map(dx)
    for p in sorted(posts_of(dx), key=lambda x: x['attributes'].get('number', 0)):
        if p['attributes'].get('number', 0) >= frm:
            a = p['attributes']
            print(f"  #{a.get('number')} [{a.get('createdAt','')[11:16]}] {author_of(p, umx)}: {plain(a.get('contentHtml',''))[:110]}")

json.dump({'phase': 2, 'ts': TS, 'note': 'Saniti near14607 (26h watch), GG near14590, 196752/196778 purge holes, 196854 flash tail, 196799 Crios-watch, 196846/196844/196851/196853/196838 tails'},
          open(f'{EV}/check54_158b_summary.json', 'w'), ensure_ascii=False, indent=1)
print('DONE phase2')
