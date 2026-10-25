# -*- coding: utf-8 -*-
# counter_sweep.py — LONG30 v4: счётчиковый свип всего диапазона БЕЗ входа в треды.
# (Решение автора 25.10 ~23:4x UTC: «длинный шаг → 30 мин, максимум слегка перетасовать,
#  с тем же эффективным покрытием проходиться по всему диапазону, но не пытаться каждый
#  раз заглядывать внутрь каждого треда — Фларум и так по счётчикам отдаёт, есть ли
#  снесённые посты». Ответ на «бесследные» тики :25 — длинный ход больше не длинный.)
#
# Сигнатуры по дифу списковых данных (lpn=lastPostNumber, cc=commentCount):
#   lpn↑ cc↑  NEW-POSTS — обычная активность (deep только для KEY/young)
#   lpn= cc↓  DEL-SIG   — СНЕСЕННЫЕ посты (главная цель мониторинга) → deep
#   lpn↑ cc=  MIX-SIG   — пост создан и вырезан (или добавка+снос) → deep
#   lpn= cc↑  UNHIDE-SIG — восстановление/расхайд → deep
#   lpn↓      ROLLBACK  → deep
#   гэп (lpn-cc) рост    — зона сносов выросла (виден в сигнатурах выше)
#   prev-тред пропал из окна свипа → OUT-OF-WINDOW; KEY-треды — целевой GET (404 → VANISH);
#   новый id (createdAt ≤3h вне KNOWN) → NEW-THREAD (near=1 верификация OP).
# Глубокий заход (near=999999 / near=1) ТОЛЬКО флагнутым, ≤8 за проход (бюджет ≤7 мин).
# Канон #48 (196411, sha256 e352e6a1…) + GG-якоря (195574#69, 195660#387, 159759#14590) —
# каждый 4-й проход (счётчик pass_no) или внепланово при DEL-SIG в их тредах.
# Состояние: /tmp/prev_lpn_<N+1>.json (цепочка rescan-эры продолжается, +поле lpa) +
# output/08_monitoring/long30_state.json (pass_no/расписание integrity) +
# state_snapshots ротация keep 2. Young-очередь НЕ трогает (линия s15/s35).
import json, os, glob, re, time, hashlib, urllib.request

TS = time.strftime('%Y%m%d_%H%M', time.gmtime())

def _hms_ago(hours):
    return time.strftime('%Y-%m-%dT%H:%M', time.gmtime(time.time() - hours * 3600))


OUT = '/home/z/my-project/output/evidence_post'
MON = '/home/z/my-project/output/08_monitoring'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
CANON48 = 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e'
KEY = {196452, 196488, 196480, 196511, 196424, 196425, 196411, 196461, 196435, 196428,
       196283, 196078, 196062, 196315, 196415, 195574, 195660, 195192, 159759,
       196852, 194758, 196524, 196475}
DEEP_CAP = 8
SWEEP_PAGES = 5          # 5 × page[size]=50 = 250 тредов по -lastPostedAt
NEW_H = 3                # NEW-THREAD: createdAt ≤3h
OWW_RECENT_H = 48        # OUT-OF-WINDOW с lpa свежее → целевой GET (кандидат VANISH)
cutover3h = _hms_ago(NEW_H)
recency_cut = _hms_ago(OWW_RECENT_H)

def get(url, name, validate_json=True):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}')
        return jload(name) if validate_json else None
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        if validate_json:
            d = json.loads(body)
            print(f'OK {name} ({len(body)}B)')
            return d
        print(f'OK {name} ({len(body)}B)')
        return True
    except Exception as e:
        print(f'FAIL {name}: {e}')
        if os.path.exists(path):
            os.remove(path)
        return None

def jload(name):
    try:
        return json.load(open(os.path.join(OUT, name)))
    except Exception:
        return None

def known_union():
    kn = set()
    for pat in ('/tmp/prev_lpn_*.json', os.path.join(MON, 'state_snapshots', 'prev_lpn_*.json')):
        for f in glob.glob(pat):
            try:
                kn |= {int(k) for k in json.load(open(f)).keys()}
            except Exception:
                pass
    try:
        y = json.load(open(os.path.join(MON, 'young_threads.json')))
        th = y.get('threads', {})
        if isinstance(th, dict):
            kn |= {int(k) for k in th.keys()}
        for it in (y.get('graduated') or []):
            if isinstance(it, dict) and it.get('id'):
                kn.add(int(it['id']))
            elif isinstance(it, (int, str)):
                kn.add(int(it))
    except Exception:
        pass
    return kn

def newest_prev():
    best = (0, None)
    for f in (glob.glob('/tmp/prev_lpn_*.json') +
              glob.glob(os.path.join(MON, 'state_snapshots', 'prev_lpn_*.json'))):
        m = re.search(r'prev_lpn_(\d+)\.json$', f)
        if m and int(m.group(1)) > best[0]:
            best = (int(m.group(1)), f)
    if not best[1]:
        return 0, {}
    try:
        return best[0], json.load(open(best[1]))
    except Exception:
        return best[0], {}

def load_state():
    try:
        return json.load(open(os.path.join(MON, 'long30_state.json')))
    except Exception:
        return {'pass_no': 0, 'last_pass_utc': None}

def norm_prev(v):
    if isinstance(v, int):
        return {'lpn': v, 'cc': None, 'lpa': None}
    if isinstance(v, dict):
        return {'lpn': v.get('lpn'), 'cc': v.get('cc'), 'lpa': v.get('lpa')}
    return None

def sig_of(pl, pc, cl, ccn):
    """(label, deep?) по дельтам; None = чисто."""
    if pl is None or cl is None:
        return None
    dl, dc = cl - pl, (ccn or 0) - (pc or 0)
    if dl < 0:
        return ('ROLLBACK', True)
    if dl == 0 and dc < 0:
        return ('DEL-SIG', True)      # снос постов без новых — ядро мониторинга
    if dl > 0 and dc <= 0:
        return ('MIX-SIG', True)      # добавка+снос/мгновенный вырез
    if dl == 0 and dc > 0:
        return ('UNHIDE-SIG', True)
    if dl > 0 and dc > 0:
        return ('NEW-POSTS', False)   # deep решает вызывающий контекст (KEY/young)
    return None

def parse_disc(d):
    items = (d or {}).get('data') or []
    out = {}
    for i in items:
        if isinstance(i, dict) and i.get('type') == 'discussions':
            a = i.get('attributes', {})
            try:
                tid = int(i.get('id'))
            except Exception:
                continue
            out[tid] = {'lpn': a.get('lastPostNumber'), 'cc': a.get('commentCount'),
                        'lpa': (a.get('lastPostedAt') or '')[:16],
                        'created': (a.get('createdAt') or '')[:16],
                        'title': (a.get('title') or '')[:70]}
    return out

state = load_state()
pass_no = int(state.get('pass_no', 0)) + 1
prev_n, prev_raw = newest_prev()
prev = {}
for k, v in prev_raw.items():
    try:
        prev[int(k)] = norm_prev(v)
    except Exception:
        pass
known = known_union()
force_integrity = bool(state.get('force_integrity'))

print(f'===== LONG30 SWEEP pass#{pass_no} {TS} UTC | база prev_lpn_{prev_n} ({len(prev)} кл) =====')

# --- 1) свип диапазона (list-only) ---
cur = {}
for off in range(0, SWEEP_PAGES * 50, 50):
    d = get(f'{BASE}/api/discussions?sort=-lastPostedAt&page[size]=50&page[offset]={off}',
            f'sweep_lpa_off{off}_{TS}.json')
    cur.update(parse_disc(d))
    time.sleep(1)
d = get(f'{BASE}/api/discussions?sort=-createdAt&page[size]=50&page[offset]=0',
        f'sweep_crea_off0_{TS}.json')
crea = parse_disc(d)
time.sleep(1)
print(f'свин: {len(cur)} тредов в окне top-{SWEEP_PAGES * 50} (-lastPostedAt) + {len(crea)} (-createdAt)')

# --- 2) диф сигнатур ---
events, flagged = [], []   # flagged: (prio, tid, why)
n_sig = 0
for tid, c in sorted(cur.items()):
    p = prev.get(tid)
    if not p:
        if tid not in known and c['created'] and c['created'] >= cutover3h:
            events.append(f'NEW-THREAD [{tid}] {c["created"]} lpn/cc {c["lpn"]}/{c["cc"]} :: {c["title"]}')
            flagged.append((1, tid, 'NEW'))
        continue
    s = sig_of(p['lpn'], p['cc'], c['lpn'], c['cc'])
    if not s:
        continue
    label, deep = s
    n_sig += 1
    gap_old = (p['lpn'] or 0) - (p['cc'] or 0)
    gap_new = (c['lpn'] or 0) - (c['cc'] or 0)
    extra = f' гэп {gap_old}->{gap_new}' if gap_new != gap_old else ''
    events.append(f'{label} [{tid}] lpn {p["lpn"]}->{c["lpn"]} cc {p["cc"]}->{c["cc"]}{extra} :: {c["title"]}')
    if deep:
        flagged.append((0 if label in ('DEL-SIG', 'MIX-SIG', 'ROLLBACK') else 2, tid, label))
    elif tid in KEY:
        flagged.append((3, tid, 'KEY-NEW-POSTS'))
    if label in ('DEL-SIG', 'MIX-SIG') and tid in (196411, 195660, 195574, 159759):
        force_integrity = True

# OUT-OF-WINDOW: в prev, но не в свипе
oww, oww_checked = [], 0
for tid, p in sorted(prev.items()):
    if tid in cur:
        continue
    oww.append(tid)
    lpa = p.get('lpa') or ''
    recent = bool(lpa) and lpa >= recency_cut
    if tid in KEY or recent:
        oww_checked += 1
        dd = get(f'{BASE}/api/discussions/{tid}?page[near]=999999',
                 f'discussion_{tid}_near999999_{TS}.json')
        time.sleep(1)
        if not dd:
            events.append(f'OWW-FAIL [{tid}] целевой GET не удался (сеть?) — остаётся на старых значениях')
            continue
        a = (dd.get('data') or {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
        if not a:
            events.append(f'VANISH-SIG [{tid}] 404 вне окна свипа (lpa было {lpa or "?"}) — 404×1')
            flagged.append((0, tid, 'VANISH'))
            continue
        cl, ccn = a.get('lastPostNumber'), a.get('commentCount')
        cur[tid] = {'lpn': cl, 'cc': ccn, 'lpa': (a.get('lastPostedAt') or '')[:16],
                    'created': (a.get('createdAt') or '')[:16], 'title': (a.get('title') or '')[:70]}
        s = sig_of(p['lpn'], p['cc'], cl, ccn)
        if s:
            label, deep = s
            n_sig += 1
            events.append(f'{label} [KEY/OWW {tid}] lpn {p["lpn"]}->{cl} cc {p["cc"]}->{ccn}')
            if deep:
                flagged.append((0, tid, label))
if oww:
    tail = ','.join(str(t) for t in oww[:12])
    print(f'OUT-OF-WINDOW: {len(oww)} тредов вне top-250 ({tail}{"..." if len(oww) > 12 else ""}); целевой GET: {oww_checked}')

# --- 3) глубокий заход только флагнутым (cap 8) ---
deep_done = []
deep_queue = sorted(f for f in flagged if f[2] != 'VANISH')[:DEEP_CAP]  # 404 VANISH уже зафиксирован
for prio, tid, why in deep_queue:
    near = 1 if why == 'NEW' else 999999
    dd = get(f'{BASE}/api/discussions/{tid}?page[near]={near}',
             f'discussion_{tid}_near{near}_{TS}.json')
    time.sleep(1)
    if not dd:
        continue
    deep_done.append(tid)
    a = (dd.get('data') or {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
    if why == 'NEW':
        users = {u.get('id'): u.get('attributes', {}).get('username')
                 for u in dd.get('included', []) if u.get('type') == 'users'}
        op = next((users.get(p.get('relationships', {}).get('user', {}).get('data', {}).get('id'))
                   for p in dd.get('included', []) if p.get('type') == 'posts'
                   and p.get('attributes', {}).get('number') == 1), '?')
        print(f'>>> NEW-VERIFY [{tid}] OP={op} lpn/cc={a.get("lastPostNumber")}/{a.get("commentCount")} :: {a.get("title", "")[:70]}')
        continue
    posts = sorted((p for p in dd.get('included', []) if p.get('type') == 'posts'
                    and p.get('attributes', {}).get('number')),
                   key=lambda p: p['attributes']['number'])[-6:]
    nums = [p['attributes']['number'] for p in posts]
    for p in posts:
        pa = p['attributes']
        hid = ' HIDDEN' if pa.get('isHidden') else ''
        txt = re.sub(r'<[^>]+>', ' ', pa.get('contentPlain') or pa.get('contentHtml') or '')[:90]
        txt = re.sub(r'\s+', ' ', txt).strip()
        print(f'    #{pa["number"]} {pa.get("createdAt", "")[:16]}{hid} :: {txt}')
    if len(nums) >= 2:
        missing = [i for i in range(nums[0], nums[-1] + 1) if i not in nums]
        if missing:
            print(f'    гэп в хвосте [{tid}]: {missing}')

# --- 4) integrity: канон #48 + GG-якоря (каждый 4-й проход или по DEL-SIG) ---
do_integrity = force_integrity or (pass_no % 4 == 0)
if do_integrity:
    print(f'===== INTEGRITY pass#{pass_no} (канон + GG-якоря) =====')
    d = get(f'{BASE}/api/posts?filter[discussion]=196411&page[size]=20&page[offset]=40',
            f'postsindex_196411_off40_{TS}.json')
    time.sleep(1)
    ok = False
    for p in ((d or {}).get('data') or []):
        if p.get('type') == 'posts' and p.get('attributes', {}).get('number') == 48:
            h = hashlib.sha256((p['attributes'].get('contentHtml') or '').encode()).hexdigest()
            ok = (h == CANON48)
            print(f'>>> CANON #48 196411: {"MATCH" if ok else "MISMATCH sha256=" + h[:16]}')
    if d is None:
        print('>>> CANON #48 196411: postsindex off40 недоступен — повтор на след. проходе')
    for tid, near, want in ((195574, 69, [69]), (195660, 381, [387]), (159759, 14590, [14590, 14591])):
        dd = get(f'{BASE}/api/discussions/{tid}?page[near]={near}',
                 f'discussion_{tid}_near{near}_{TS}.json')
        time.sleep(1)
        if not dd:
            continue
        found = {p['attributes']['number']: p['attributes'] for p in dd.get('included', [])
                 if p.get('type') == 'posts' and p.get('attributes', {}).get('number') in want}
        for w in want:
            if w in found:
                fa = found[w]
                print(f'>>> GG [{tid}] #{w} alive hidden={fa.get("isHidden")} :: {re.sub(r"<[^>]+>", " ", fa.get("contentPlain") or fa.get("contentHtml") or "")[:60]}')
            else:
                print(f'>>> GG [{tid}] #{w} НЕ НАЙДЕН в окне near={near} — проверить вручную')

# --- 5) новое состояние: prev_lpn_{N+1} + long30_state + ротация снапшотов ---
newn = prev_n + 1
newprev = {}
for tid, c in cur.items():
    if c['lpn'] is not None:
        newprev[str(tid)] = {'lpn': c['lpn'], 'cc': c['cc'], 'lpa': c['lpa']}
for tid, p in prev.items():          # вне окна (вкл. VANISH) сохраняем старые значения
    if tid not in cur:
        newprev[str(tid)] = {'lpn': p['lpn'], 'cc': p['cc'], 'lpa': p.get('lpa')}
json.dump(newprev, open(f'/tmp/prev_lpn_{newn}.json', 'w'))
snap_dir = os.path.join(MON, 'state_snapshots')
os.makedirs(snap_dir, exist_ok=True)
json.dump(newprev, open(os.path.join(snap_dir, f'prev_lpn_{newn}.json'), 'w'))
old_snaps = sorted(glob.glob(os.path.join(snap_dir, 'prev_lpn_*.json')),
                   key=lambda f: int(re.search(r'(\d+)\.json$', f).group(1)))
for f in old_snaps[:-2]:
    os.remove(f)
state.update({'pass_no': pass_no, 'last_pass_utc': TS, 'prev_n': newn,
              'force_integrity': False})
json.dump(state, open(os.path.join(MON, 'long30_state.json'), 'w'), ensure_ascii=False, indent=1)

print(f'>>> SWEEP ИТОГ pass#{pass_no}: окно {len(cur)}, дельт-сигнатур {n_sig}, '
      f'глубоких заходов {len(deep_done)} {deep_done}, OWW {len(oww)} (проверено {oww_checked}), '
      f'integrity={"ДА" if do_integrity else "нет"}')
print(f'>>> prev_lpn_{newn}.json записан ({len(newprev)} кл; /tmp + state_snapshots keep 2)')
for e in events:
    print(f'>>> {e}')
print(f'DONE LONG30 pass#{pass_no} {TS}')
