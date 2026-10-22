import json, os, urllib.request, time, re

TS = '20261022_1830'
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

# ---- 0) NEW x4: OP near=1 (БЕЗ include — урок 54-131) + хвост near=999999 ----
print('== NEW x4: 196865 «Несчастье за несчастьем. Реорганизация 😔» (cc=19!) + 196867 «А что с серверами?» + 196864 «Крашит игру» + 196870 «Это не я)» ==')
for tid, frm in ((196865, 1), (196867, 1), (196864, 1), (196870, 1)):
    try:
        fop = fetch(tid, 1, 'OP')
        dop = load(fop)
        ums = users_map(dop)
        ppo = sorted(posts_of(dop), key=lambda x: x['attributes'].get('number', 0))
        dattr = dop.get('data', {}).get('attributes', {}) if isinstance(dop.get('data'), dict) else {}
        print(f'-- d/{tid}: OP + metadata (cc={dattr.get("commentCount")} LPN={dattr.get("lastPostNumber")} createdAt={dattr.get("createdAt","?")[:16]}) --')
        for p in ppo:
            a = p['attributes']
            print(f"  OP #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, ums)}: {plain(a.get('contentHtml',''))[:400]}")
            break
        ftt = fetch(tid, 999999, 'TAIL')
        dtt = load(ftt)
        umst = users_map(dtt)
        ptt = sorted(posts_of(dtt), key=lambda x: x['attributes'].get('number', 0))
        dattr2 = dtt.get('data', {}).get('attributes', {}) if isinstance(dtt.get('data'), dict) else {}
        print(f'-- d/{tid} хвост: cc={dattr2.get("commentCount")} LPN={dattr2.get("lastPostNumber")} --')
        for p in ptt:
            a = p['attributes']
            if a.get('number', 0) >= frm:
                print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, umst)}: {plain(a.get('contentHtml',''))[:160]}")
    except Exception as e:
        print(f'  NEW d/{tid} FAIL: {e}')

# ---- 1) Санити: near=14610 (29-й час; Crios вернулся?) ----
print('== САНИТИ 159759 near=14610: 29-Й ЧАС (LPN=14610 на 17:30; Crios НЕТ с 11:53 7+ ч) ==')
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

# ---- 2) GG-якоря: near=14590 (19-Й ЧАС, база 18:30) ----
print('== GG-ЯКОРЯ near=14590 (19-Й ЧАС, база 18:30) ==')
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

# ---- 3) 191642: свежий хвост near=312 (разгон 294->312, +18/час — спор стат-лимита) ----
print('== 191642 ОБВЕСЫ-РАЗГОН: near=312 свежий (294->312 +18/час; Crios ×3 vs WindReaper/Shmendergar) ==')
try:
    f191 = fetch(191642, 312, 'TAIL-NEW')
    d191 = load(f191)
    um191 = users_map(d191)
    da191 = d191.get('data', {}).get('attributes', {}) if isinstance(d191.get('data'), dict) else {}
    p191 = sorted(posts_of(d191), key=lambda x: x['attributes'].get('number', 0))
    print(f"  cc={da191.get('commentCount')} LPN={da191.get('lastPostNumber')}")
    for p in p191:
        a = p['attributes']
        if a.get('number', 0) >= 303:
            print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, um191)}: {plain(a.get('contentHtml',''))[:150]}")
except Exception as e:
    print(f'  191642 FAIL: {e}')

# ---- 4) 196862: свежий хвост near=18 (эскалация: пермач/снос? Crios?) ----
print('== 196862 ПОЧЕМУ БЫ И ДА: near=18 свежий (эскалация 18; Crios молчит с #10 16:42) ==')
try:
    f862 = fetch(196862, 18, 'TAIL-NEW')
    d862 = load(f862)
    um862 = users_map(d862)
    da862 = d862.get('data', {}).get('attributes', {}) if isinstance(d862.get('data'), dict) else {}
    p862 = sorted(posts_of(d862), key=lambda x: x['attributes'].get('number', 0))
    print(f"  cc={da862.get('commentCount')} LPN={da862.get('lastPostNumber')} locked={da862.get('isLocked')}")
    for p in p862:
        a = p['attributes']
        if a.get('number', 0) >= 17:
            print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, um862)}: {plain(a.get('contentHtml',''))[:160]}")
except Exception as e:
    print(f'  196862 FAIL: {e}')

# ---- 5) 196856: свежий хвост near=42 (solved? тайник 7?) + дыро из run1-снапа ----
print('== 196856 СУМАТОХА В БАРЕ: near=42 свежий + дыро (cc=39/LPN=41 на 17:30 — 2 выреза) ==')
try:
    f856 = fetch(196856, 42, 'TAIL-NEW')
    d856 = load(f856)
    um856 = users_map(d856)
    da856 = d856.get('data', {}).get('attributes', {}) if isinstance(d856.get('data'), dict) else {}
    p856 = sorted(posts_of(d856), key=lambda x: x['attributes'].get('number', 0))
    print(f"  cc={da856.get('commentCount')} LPN={da856.get('lastPostNumber')}")
    for p in p856:
        a = p['attributes']
        if a.get('number', 0) >= 41:
            print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, um856)}: {plain(a.get('contentHtml',''))[:150]}")
    f856r = f'{EV}/discussion_196856_near999999_{TS}.json'
    if os.path.exists(f856r):
        d856r = load(f856r)
        nums856 = sorted(p['attributes'].get('number') for p in posts_of(d856r) if isinstance(p.get('attributes'), dict) and p['attributes'].get('number'))
        holes = [n for n in range(1, (nums856[-1] if nums856 else 0) + 1) if n not in set(nums856)]
        print(f'  run1-снап дыры (1..LPN отсутствуют в хвосте): {holes}')
except Exception as e:
    print(f'  196856 FAIL: {e}')

# ---- 6) хвосты живых: свежие near=<LPN> для выросших + run1-снапы для остальных ----
print('== ХВОСТЫ свежие: 196846 (>=27, +8 «Ап»-вспышка), 196854 (>=69, jlococen-диалог), 196777 (>=66), 196772 (>=41) ==')
for tid, near, frm in ((196846, 35, 27), (196854, 75, 69), (196777, 73, 66), (196772, 48, 41)):
    try:
        fx = fetch(tid, near, 'TAIL-NEW')
        dx = load(fx)
        umx = users_map(dx)
        dax = dx.get('data', {}).get('attributes', {}) if isinstance(dx.get('data'), dict) else {}
        pxx = sorted(posts_of(dx), key=lambda x: x['attributes'].get('number', 0))
        print(f'-- d/{tid}: cc={dax.get("commentCount")} LPN={dax.get("lastPostNumber")} --')
        for p in pxx:
            a = p['attributes']
            if a.get('number', 0) >= frm:
                print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, umx)}: {plain(a.get('contentHtml',''))[:140]}")
    except Exception as e:
        print(f'  d/{tid} FAIL: {e}')

print('== ХВОСТЫ из run1-снапов: 196799 (>=115), 196842 (>=42), 196810 (>=80), 196838 (>=27), 196839 (>=35), 196857 (>=18), 196844 (>=32), 196851 (>=8), 196832 (>=97), 196861 (>=2), 196853 (>=21) ==')
for tid, frm in ((196799, 115), (196842, 42), (196810, 80), (196838, 27), (196839, 35), (196857, 18), (196844, 32), (196851, 8), (196832, 97), (196861, 2), (196853, 21)):
    fnx = f'{EV}/discussion_{tid}_near999999_{TS}.json'
    if not os.path.exists(fnx):
        print(f'== d/{tid}: (снапа нет) =='); continue
    print(f'== d/{tid}: авторы хвоста (>=#{frm}) ==')
    try:
        dx = load(fnx)
        umx = users_map(dx)
        for p in sorted(posts_of(dx), key=lambda x: x['attributes'].get('number', 0)):
            if p['attributes'].get('number', 0) >= frm:
                a = p['attributes']
                print(f"  #{a.get('number')} [{a.get('createdAt','')[11:19]}] {author_of(p, umx)}: {plain(a.get('contentHtml',''))[:110]}")
    except Exception as e:
        print(f'  d/{tid} FAIL: {e}')

# ---- 7) cc-контроль чисток: 196752 + 196778 + 196805 ----
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
print('== 196805 Диггерские байки: видимые номера (LPN=42, cc=39 — чистка СТОП 4-Й ЧАС) ==')
f805 = f'{EV}/discussion_196805_near999999_{TS}.json'
if os.path.exists(f805):
    d805 = load(f805)
    dattr = d805.get('data', {}).get('attributes', {}) if isinstance(d805.get('data'), dict) else {}
    nums = sorted(p['attributes'].get('number') for p in posts_of(d805) if isinstance(p.get('attributes'), dict))
    print(f"  cc={dattr.get('commentCount')} видимый хвост: {nums[-12:]}")
else:
    print('  (снапа нет — SKIP в run1?)')

json.dump({'phase': 2, 'ts': TS, 'note': 'NEW x4 OP+tail (196865 Reorganizacia cc19, 196867 servery, 196864 crash, 196870), Saniti near14610 (29h), GG near14590 (19h), 191642 near312 surge 294->312, 196862 near18 escalade, 196856 near42 + holes, fresh tails 196846/196854/196777/196772, run1 tails x11, purges 196752/196778/196805'},
          open(f'{EV}/check54_161b_summary.json', 'w'), ensure_ascii=False, indent=1)
print('DONE phase2')
