import json, os, urllib.request, time, re

TS = '20261022_1630'
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

# ---- 0) NEW 196862: OP near=1 (взят вручную) + near999999 ----
print('== NEW d/196862 «Почему бы и да»: OP + хвост ==')
try:
    fo = fetch(196862, 1, 'OP')
    do = load(fo)
    ums = users_map(do)
    po = sorted(posts_of(do), key=lambda p: p['attributes'].get('number', 0))
    if po:
        p0 = po[0]
        a0 = p0['attributes']
        ud = p0.get('relationships', {}).get('user', {}).get('data', {})
        dd = do.get('data', {}).get('attributes', {}) if isinstance(do.get('data'), dict) else {}
        print(f"  OP #{a0.get('number')} [{a0.get('createdAt')}] {ums.get(ud.get('id'),'?')}(uid={ud.get('id')}) cc={dd.get('commentCount','?')} title={dd.get('title','?')}")
        print(f"  OP text: {plain(a0.get('contentHtml',''))[:300]}")
    ft = fetch(196862, 999999, 'TAIL')
    dt = load(ft)
    umst = users_map(dt)
    pt = sorted(posts_of(dt), key=lambda p: p['attributes'].get('number', 0))
    print(f'  TAIL: {len(pt)} posts, номера {[p["attributes"].get("number") for p in pt]}')
    for p in pt:
        a = p['attributes']
        print(f"    #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, umst)}: {plain(a.get('contentHtml',''))[:120]}")
except Exception as e:
    print(f'  196862 FAIL: {e}')

# ---- 1) Санити: near=14609 (27-й час: новые >=14609 + авторства rel.user) ----
print('== САНИТИ 159759 near=14609: 27-Й ЧАС (LPN=14609 на 16:30 — новых после 14:54 нет? Crios вернулся? mentionedBy?) ==')
fs = fetch(159759, 14609, 'SANITI-NEW')
d = load(fs)
ums = users_map(d)
po = sorted(posts_of(d), key=lambda p: p['attributes'].get('number', 0))
print(f'  страница: {[p["attributes"].get("number") for p in po]}')
for p in po:
    if p['attributes'].get('number', 0) >= 14606:
        a = p['attributes']
        ud = p.get('relationships', {}).get('user', {}).get('data', {})
        mb = p['attributes'].get('mentionedBy', [])
        print(f"  #{a.get('number')} [{a.get('createdAt')}] {ums.get(ud.get('id'),'?')}(uid={ud.get('id')}) mentionedBy={mb}")
        print(f"     text: {plain(a.get('contentHtml',''))[:200]}")

# ---- 2) GG-якоря: near=14590 (страница 14581-14600 => #14590+#14591 одним снапом) ----
print('== GG-ЯКОРЯ near=14590 (17-Й ЧАС, база 16:30) ==')
fg = fetch(159759, 14590, 'GG')
dg = load(fg)
umg = users_map(dg)
for p in posts_of(dg):
    n = p['attributes'].get('number')
    if n in (14590, 14591):
        rx = {k: v for k, v in p['attributes'].get('reactionCounts', {}).items() if v}
        likes = [umg.get(l['id'], l['id']) for l in p.get('relationships', {}).get('likes', {}).get('data', [])]
        mb = p['attributes'].get('mentionedBy', [])
        print(f'  #{n}: likes={p["attributes"].get("likesCount")} liked_by={likes} rx_nonzero={rx} mentionedBy={mb}')

# ---- 3) 196856 ИНТЕРАКТИВ: хвост >=33 (записки Crios? solved? дыра cc vs LPN) ----
print('== 196856 СУМАТОХА В БАРЕ: авторы хвоста (>=#33), дыро-анализ cc/LPN ==')
f856 = f'{EV}/discussion_196856_near999999_{TS}.json'
if os.path.exists(f856):
    d856 = load(f856)
    ums856 = users_map(d856)
    dattr = d856.get('data', {}).get('attributes', {}) if isinstance(d856.get('data'), dict) else {}
    nums856 = sorted(p['attributes'].get('number') for p in posts_of(d856) if isinstance(p.get('attributes'), dict) and p['attributes'].get('number'))
    visible = set(nums856)
    holes = [n for n in range(1, (nums856[-1] if nums856 else 0) + 1) if n not in visible]
    print(f"  cc={dattr.get('commentCount')} LPN={dattr.get('lastPostNumber')} видимые={nums856}")
    print(f"  дыры (1..LPN отсутствуют в хвосте): {holes}")
    for p in sorted(posts_of(d856), key=lambda x: x['attributes'].get('number', 0)):
        if p['attributes'].get('number', 0) >= 31:
            a = p['attributes']
            print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, ums856)}: {plain(a.get('contentHtml',''))[:130]}")
else:
    print('  (снапа нет)')

# ---- 4) хвосты-авторы: 196854 (>=55) / 196799 (>=113) / 196842 (>=34) / 196843 (>=21) ----
print('== ХВОСТЫ: 196854 (>=55), 196799 (>=113), 196842 (>=34), 196843 (>=21) ==')
for tid, frm in ((196854, 55), (196799, 113), (196842, 34), (196843, 21)):
    fnx = f'{EV}/discussion_{tid}_near999999_{TS}.json'
    if not os.path.exists(fnx):
        print(f'== d/{tid}: (снапа нет) =='); continue
    print(f'== d/{tid}: авторы хвоста (>=#{frm}) ==')
    dx = load(fnx)
    umx = users_map(dx)
    for p in sorted(posts_of(dx), key=lambda x: x['attributes'].get('number', 0)):
        if p['attributes'].get('number', 0) >= frm:
            a = p['attributes']
            print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, umx)}: {plain(a.get('contentHtml',''))[:130]}")

# ---- 5) хвосты поменьше: 196857 (>=17), 196838 (>=25, дыро cc25/LPN27), 196839 (>=32) ----
print('== ХВОСТЫ: 196857 (>=17), 196838 (>=25), 196839 (>=32), 196844 (>=32), 196851 (>=8), 196832 (>=97), 196810 (>=77), 196861 (>=2) ==')
for tid, frm in ((196857, 17), (196838, 25), (196839, 32), (196844, 32), (196851, 8), (196832, 97), (196810, 77), (196861, 2)):
    fnx = f'{EV}/discussion_{tid}_near999999_{TS}.json'
    if not os.path.exists(fnx):
        print(f'== d/{tid}: (снапа нет) =='); continue
    print(f'== d/{tid}: авторы хвоста (>=#{frm}) ==')
    dx = load(fnx)
    umx = users_map(dx)
    dattr = dx.get('data', {}).get('attributes', {}) if isinstance(dx.get('data'), dict) else {}
    for p in sorted(posts_of(dx), key=lambda x: x['attributes'].get('number', 0)):
        if p['attributes'].get('number', 0) >= frm:
            a = p['attributes']
            print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, umx)}: {plain(a.get('contentHtml',''))[:110]}")
    if tid == 196838:
        numsx = sorted(p['attributes'].get('number') for p in posts_of(dx) if isinstance(p.get('attributes'), dict) and p['attributes'].get('number'))
        visx = set(numsx)
        holex = [n for n in range(1, (numsx[-1] if numsx else 0) + 1) if n not in visx]
        print(f"  196838 дыро-анализ: cc={dattr.get('commentCount')} LPN={dattr.get('lastPostNumber')} видимые={numsx[-8:]} дыры={holex}")

# ---- 6) cc-контроль чисток: 196752 + 196778 + 196805 (news cc=39 при LPN 40?) ----
print('== 196752 Слухи: видимые номера (LPN=28, cc=24) ==')
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
    nums = sorted(p['attributes'].get('number') for p in posts_of(d778) if isinstance(p.get('attributes'), dict))
    print(f'  видимый хвост: {nums}')
else:
    print('  (снапа нет — SKIP в run1?)')
print('== 196805 Диггерские байки: видимые номера (LPN=40, cc=38→news 39?) ==')
f805 = f'{EV}/discussion_196805_near999999_{TS}.json'
if os.path.exists(f805):
    d805 = load(f805)
    dattr = d805.get('data', {}).get('attributes', {}) if isinstance(d805.get('data'), dict) else {}
    nums = sorted(p['attributes'].get('number') for p in posts_of(d805) if isinstance(p.get('attributes'), dict))
    print(f"  cc={dattr.get('commentCount')} видимый хвост: {nums[-10:]}")
else:
    print('  (снапа нет — SKIP в run1?)')

# ---- 7) Канон #48 196411: sha256 из off20/off40 (снапы run1) ----
print('== 196411 КАНОН #48: sha256 ×2 (off20/off40, снапы 1630) ==')
for off in (20, 40):
    fc = f'{EV}/postsindex_196411_off{off}_{TS}.json'
    if not os.path.exists(fc):
        print(f'  off{off}: (файла нет)'); continue
    dc = load(fc)
    inc = dc.get('included', [])
    if isinstance(inc, dict): inc = list(inc.values())
    p48 = None
    for x in inc:
        if isinstance(x, dict) and x.get('type') == 'posts' and x.get('attributes', {}).get('number') == 48:
            p48 = x
    if p48:
        h = p48['attributes'].get('contentHtml', '')
        sha = __import__('hashlib').sha256(h.encode()).hexdigest()
        ok = 'OK' if sha == 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e' else '!!!MISMATCH'
        print(f'  off{off}: sha256={sha[:16]}... {ok}')
    else:
        print(f'  off{off}: #48 не найден')

json.dump({'phase': 2, 'ts': TS, 'note': 'Saniti near14609 (27h watch), GG near14590, 196856 interactive tail+holes, 196860 CONFIRMED 404 SNOSEN, 196862 NEW OP, tails 196854/196799/196842/196843/196857/196838/196839/196844/196851/196832/196810/196861, purges 196752/196778/196805, canon #48 sha256 x2'},
          open(f'{EV}/check54_159b_summary.json', 'w'), ensure_ascii=False, indent=1)
print('DONE phase2')
