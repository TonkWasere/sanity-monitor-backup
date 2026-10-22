import json, os, urllib.request, time, re

TS = '20261022_1730'
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
    out = {}
    inc = d.get('included', [])
    if isinstance(inc, dict): inc = [inc]
    for u in inc:
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
    inc = d.get('included', [])
    if isinstance(inc, dict): inc = [inc]
    for p in inc:
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

# ---- 0) 196862: хвост >=11 (эскалация OP снесённого 196860: 10->18, +8 за час) ----
print('== 196862 «Почему бы и да»: хвост >=#11 (ЭСКАЛАЦИЯ +8; пермач? Crios? Mr_Emka_T-тема?) ==')
try:
    ft = fetch(196862, 999999, 'TAIL')
    dt = load(ft)
    umst = users_map(dt)
    pt = sorted(posts_of(dt), key=lambda p: p['attributes'].get('number', 0))
    dattr = dt.get('data', {}).get('attributes', {}) if isinstance(dt.get('data'), dict) else {}
    print(f"  cc={dattr.get('commentCount')} LPN={dattr.get('lastPostNumber')} locked={dattr.get('isLocked')}")
    for p in pt:
        a = p['attributes']
        if a.get('number', 0) >= 11:
            print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, umst)}: {plain(a.get('contentHtml',''))[:150]}")
except Exception as e:
    print(f'  196862 FAIL: {e}')

# ---- 1) Санити: near=14610 (28-й час: новые >=14610; Crios вернулся?) ----
print('== САНИТИ 159759 near=14610: 28-Й ЧАС (LPN=14610 на 16:30; Crios НЕТ с 11:53; паки-спор LordZoHbl) ==')
try:
    fs = fetch(159759, 14610, 'SANITI-NEW')
    d = load(fs)
    ums = users_map(d)
    po = sorted(posts_of(d), key=lambda p: p['attributes'].get('number', 0))
    print(f'  страница: {[p["attributes"].get("number") for p in po]}')
    for p in po:
        if p['attributes'].get('number', 0) >= 14608:
            a = p['attributes']
            ud = p.get('relationships', {}).get('user', {}).get('data', {})
            mb = a.get('mentionedBy', [])
            print(f"  #{a.get('number')} [{a.get('createdAt')}] {ums.get(ud.get('id'),'?')}(uid={ud.get('id')}) mentionedBy={mb}")
            print(f"     text: {plain(a.get('contentHtml',''))[:200]}")
except Exception as e:
    print(f'  Санити FAIL: {e}')

# ---- 2) GG-якоря: near=14590 (18-Й ЧАС, база 17:30) ----
print('== GG-ЯКОРЯ near=14590 (18-Й ЧАС, база 17:30) ==')
try:
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
except Exception as e:
    print(f'  GG FAIL: {e}')

# ---- 3) 196856 ИНТЕРАКТИВ: хвост >=39 (записки? solved? награды-гнев?) + дыро ----
print('== 196856 СУМАТОХА В БАРЕ: авторы хвоста (>=#39), дыро-анализ cc/LPN ==')
try:
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
            if p['attributes'].get('number', 0) >= 39:
                a = p['attributes']
                print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, ums856)}: {plain(a.get('contentHtml',''))[:140]}")
    else:
        print('  (снапа нет)')
except Exception as e:
    print(f'  196856 FAIL: {e}')

# ---- 4) хвосты-авторы: 196854 (>=63) / 196799 (>=115) / 196842 (>=40) / 196846 (>=26) ----
print('== ХВОСТЫ: 196854 (>=63), 196799 (>=115), 196842 (>=40), 196846 (>=26) ==')
for tid, frm in ((196854, 63), (196799, 115), (196842, 40), (196846, 26)):
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

# ---- 5) хвосты поменьше + NEW-волна обвесов 191642 + 196795 дыро ----
print('== ХВОСТЫ: 196857 (>=18), 196838 (>=27), 196839 (>=35), 196844 (>=32), 196851 (>=8), 196832 (>=97), 196810 (>=77), 196861 (>=2) ==')
for tid, frm in ((196857, 18), (196838, 27), (196839, 35), (196844, 32), (196851, 8), (196832, 97), (196810, 77), (196861, 2)):
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

print('== 191642 обвесы-разгон: near999999 (утром 265 -> фронт 291 на 17:23, +26 за 6 ч) ==')
try:
    f191 = fetch(191642, 999999, 'TAIL')
    d191 = load(f191)
    um191 = users_map(d191)
    da191 = d191.get('data', {}).get('attributes', {}) if isinstance(d191.get('data'), dict) else {}
    p191 = sorted(posts_of(d191), key=lambda x: x['attributes'].get('number', 0))
    print(f"  cc={da191.get('commentCount')} LPN={da191.get('lastPostNumber')}")
    for p in p191[-8:]:
        a = p['attributes']
        print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, um191)}: {plain(a.get('contentHtml',''))[:130]}")
except Exception as e:
    print(f'  191642 FAIL: {e}')

print('== 196795 Зона в кадре: near999999 (фронт cc=14 при LPN=15 — вырез? #SZFRAGMENTS 28.10) ==')
try:
    f795 = fetch(196795, 999999, 'TAIL')
    d795 = load(f795)
    um795 = users_map(d795)
    da795 = d795.get('data', {}).get('attributes', {}) if isinstance(d795.get('data'), dict) else {}
    p795 = sorted(posts_of(d795), key=lambda x: x['attributes'].get('number', 0))
    nums795 = [p['attributes'].get('number') for p in p795]
    holes795 = [n for n in range(1, (nums795[-1] if nums795 else 0) + 1) if n not in set(nums795)]
    print(f"  cc={da795.get('commentCount')} LPN={da795.get('lastPostNumber')} видимые={nums795} дыры={holes795}")
    for p in p795[-4:]:
        a = p['attributes']
        print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, um795)}: {plain(a.get('contentHtml',''))[:130]}")
except Exception as e:
    print(f'  196795 FAIL: {e}')

# ---- 6) cc-контроль чисток: 196752 + 196778 + 196805 ----
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
print('== 196805 Диггерские байки: видимые номера (LPN=42, cc=39 — ТРЕТИЙ ВЫРЕЗ) ==')
f805 = f'{EV}/discussion_196805_near999999_{TS}.json'
if os.path.exists(f805):
    d805 = load(f805)
    dattr = d805.get('data', {}).get('attributes', {}) if isinstance(d805.get('data'), dict) else {}
    nums = sorted(p['attributes'].get('number') for p in posts_of(d805) if isinstance(p.get('attributes'), dict))
    print(f"  cc={dattr.get('commentCount')} видимый хвост: {nums[-12:]}")
else:
    print('  (снапа нет — SKIP в run1?)')

json.dump({'phase': 2, 'ts': TS, 'note': 'Saniti near14610 (28h watch), GG near14590 (18h), 196862 tail +8 escalade, 196856 tail+holes, 196854/196799/196842/196846 tails, 196857/196838/196839/196844/196851/196832/196810/196861 tails, NEW 191642 obvesy surge (265->291), 196795 hole-check, purges 196752/196778/196805'},
          open(f'{EV}/check54_160b_summary.json', 'w'), ensure_ascii=False, indent=1)
print('DONE phase2')
