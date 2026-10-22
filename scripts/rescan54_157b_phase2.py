import json, os, urllib.request, time, re

TS = '20261022_1430'
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

# ---- 1) NEW x3: 196851 / 196853 / 196854 — OP near=1 + tail near999999 ----
for tid in (196851, 196853, 196854):
    print(f'== NEW d/{tid}: OP near=1 + near999999 ==')
    fo = fetch(tid, 1, 'OP')
    do = load(fo)
    ums = users_map(do)
    po = sorted(posts_of(do), key=lambda p: p['attributes'].get('number', 0))
    if po:
        p0 = po[0]
        a0 = p0['attributes']
        ud = p0.get('relationships', {}).get('user', {}).get('data', {})
        cc = do.get('data', {}).get('attributes', {}) if isinstance(do.get('data'), dict) else {}
        print(f"  OP #{a0.get('number')} [{a0.get('createdAt')}] {ums.get(ud.get('id'),'?')}(uid={ud.get('id')}) cc={a0.get('cc','?')}")
        print(f"  OP text: {plain(a0.get('contentHtml',''))[:220]}")
        for p in po[1:4]:
            a = p['attributes']
            print(f"    #{a.get('number')} [{a.get('createdAt','')[11:16]}] {author_of(p, ums)}: {plain(a.get('contentHtml',''))[:100]}")
    ft = fetch(tid, 999999, 'TAIL')
    dt = load(ft)
    umst = users_map(dt)
    pt = sorted(posts_of(dt), key=lambda p: p['attributes'].get('number', 0))
    print(f'  TAIL: {len(pt)} posts, номера {[p["attributes"].get("number") for p in pt]}')
    for p in pt[-6:]:
        a = p['attributes']
        print(f"    #{a.get('number')} [{a.get('createdAt','')[11:16]}] {author_of(p, umst)}: {plain(a.get('contentHtml',''))[:100]}")

# ---- 2) Санити: near=14602 (страница 14601-14620 => #14601-#14604 + авторства) ----
print('== САНИТИ 159759 near=14602: новые #14603/#14604 + авторства ==')
fs = fetch(159759, 14602, 'SANITI-NEW')
d = load(fs)
ums = users_map(d)
po = sorted(posts_of(d), key=lambda p: p['attributes'].get('number', 0))
print(f'  страница: {[p["attributes"].get("number") for p in po]}')
for p in po:
    if p['attributes'].get('number', 0) >= 14601:
        a = p['attributes']
        ud = p.get('relationships', {}).get('user', {}).get('data', {})
        print(f"  #{a.get('number')} [{a.get('createdAt')}] {ums.get(ud.get('id'),'?')}(uid={ud.get('id')})")
        print(f"     text: {plain(a.get('contentHtml',''))[:240]}")

# ---- 3) GG-якоря: near=14590 (страница 14581-14600 => #14590+#14591 одним снапом) ----
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

# ---- 4) cc-LPN расхождения: 196752 (24/28) + 196778 (52/54) — какие номера вырезаны ----
print('== 196752 Слухи: видимые номера (LPN=28, cc=24 — найти дыры) ==')
d752 = load(f'{EV}/discussion_196752_near999999_{TS}.json')
nums = sorted(p['attributes'].get('number') for p in posts_of(d752) if isinstance(p.get('attributes'), dict))
print(f'  видимый хвост: {nums}')
print('== 196778 Цепь Распада: видимые номера (LPN=54, cc=52) ==')
d778 = load(f'{EV}/discussion_196778_near999999_{TS}.json')
ums778 = users_map(d778)
nums = sorted(p['attributes'].get('number') for p in posts_of(d778) if isinstance(p.get('attributes'), dict))
print(f'  видимый хвост: {nums}')
for p in posts_of(d778):
    if p['attributes'].get('number', 0) >= 50:
        a = p['attributes']
        print(f"  #{a.get('number')} [{a.get('createdAt','')[5:16]}] {author_of(p, ums778)}: {plain(a.get('contentHtml',''))[:110]}")

# ---- 5) 196799 рейтинг-спор: кто пишет #101-112 (Crios?) ----
print('== 196799 (LPN 112, +13): авторы хвоста ==')
d799 = load(f'{EV}/discussion_196799_near999999_{TS}.json')
ums799 = users_map(d799)
for p in sorted(posts_of(d799), key=lambda x: x['attributes'].get('number', 0)):
    n = p['attributes'].get('number', 0)
    if n >= 101:
        a = p['attributes']
        print(f"  #{n} [{a.get('createdAt','')[11:16]}] {author_of(p, ums799)}: {plain(a.get('contentHtml',''))[:110]}")

# ---- 6) 196844/196846/196838 хвосты: авторы новых постов ----
for tid, frm in ((196844, 23), (196846, 14), (196838, 18)):
    print(f'== d/{tid}: авторы хвоста (>=#{frm}) ==')
    dx = load(f'{EV}/discussion_{tid}_near999999_{TS}.json')
    umx = users_map(dx)
    for p in sorted(posts_of(dx), key=lambda x: x['attributes'].get('number', 0)):
        if p['attributes'].get('number', 0) >= frm:
            a = p['attributes']
            print(f"  #{a.get('number')} [{a.get('createdAt','')[11:16]}] {author_of(p, umx)}: {plain(a.get('contentHtml',''))[:110]}")

json.dump({'phase': 2, 'ts': TS, 'note': 'NEWx3 OP+tails, Saniti 14601-14604, GG near14590, 196752/196778 holes, 196799/196844/196846/196838 tails'},
          open(f'{EV}/check54_157b_summary.json', 'w'), ensure_ascii=False, indent=1)
print('DONE phase2')
