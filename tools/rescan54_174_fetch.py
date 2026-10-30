# rescan54_174_fetch.py — Task 54-174: часовой cron-раунд ~13:28 UTC 23.10 (ЧЕТВЁРТЫЙ час подряд БЕЗ WIPE:
# healthcheck 13:28 = 12/12, HEAD bc2167f2 = origin = backup, prev_lpn_174 цел 75 ключей). Окно 1 ч:
# 12:30->13:30 (54-173 закрыт ~12:44). Watch-list из №213: целотредовый снос 196887 (cc=213, ~250 постов
# за 6 ч)?; догонит ли 196894 ритм 196411 (3-й вырез вернулся)?; первые вырезы в 196896/196898?;
# 196893 вирус 4-й час?; 196867 после оживления?; 196874 2-й вырез; Crios 16+ ч; @Рупоры ~17-18 ч;
# ОТС-итоги X+3; Санити 47-й; канон 46-й; 404 82-й; Празднество 28.10; PAT №48
import json, os, urllib.request, time, hashlib, re

TS = '20261023_1330'
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
CANON48 = 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e'
WIN = '2026-10-23T12:30'  # окно 1 ч (54-173 закрыт ~12:44)

def get(url, name, validate_json=True):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}'); return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        if validate_json:
            json.loads(body)
        print(f'OK {name} ({len(body)}B)')
        return True
    except Exception as e:
        print(f'FAIL {name}: {e}')
        if os.path.exists(path): os.remove(path)
        return False

def disc_items(fname):
    try:
        d = json.load(open(os.path.join(OUT, fname)))
    except Exception as e:
        print(f'PARSE FAIL {fname}: {e}'); return []
    out = []
    data = d.get('data')
    for i in (data if isinstance(data, list) else [data] if data else []):
        if isinstance(i, dict) and i.get('type') == 'discussions':
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'discussions':
            out.append(i)
    return out

def posts_of(fname):
    try:
        d = json.load(open(os.path.join(OUT, fname)))
    except Exception as e:
        print(f'PARSE FAIL {fname}: {e}'); return []
    data = d.get('data')
    items = data if isinstance(data, list) else [data] if data else []
    out = []
    for i in items:
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    return out

def head_text(p, n=110):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or ''
    if not t:
        t = a.get('contentHtml') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

def thread_summary(tid, near='999999'):
    fn = f'discussion_{tid}_near{near}_{TS}.json'
    pp = posts_of(fn)
    try:
        dd = json.load(open(os.path.join(OUT, fn)))
        aa = dd.get('data', {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
        print(f"[{tid}] cc={aa.get('commentCount')} lastPostNumber={aa.get('lastPostNumber')} sticky={aa.get('sticky')} locked={aa.get('isLocked')}")
    except Exception as e:
        print(f'[{tid}] attrs fail ({e}) — 404/снос?')
        return []
    tail = sorted(pp, key=lambda p: p.get('attributes', {}).get('number') or 0)[-6:]
    for p in tail:
        a = p.get('attributes', {})
        print(f"  #{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")
    return pp

# === ФАЗА 1: витрина + фронт + ТГК + search ===
get(f'{BASE}/api/discussions?filter[tag]=news&sort=-lastPostedAt&page[size]=50&page[offset]=0', f'tagnews_off0_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions?page[offset]=0', f'frontindex_off0_{TS}.json'); time.sleep(1)
get('https://t.me/s/stalzone', f'tg_stalzone_page0_{TS}.html', validate_json=False); time.sleep(1)
get('https://t.me/s/spectrum_zone', f'tg_spectrum_page0_{TS}.html', validate_json=False); time.sleep(1)
get(f'{BASE}/api/discussions?filter[q]=%D0%BB%D0%B5%D0%B3%D0%B5%D0%BD%D0%B4%D0%B0&page[offset]=0', f'search_legenda_{TS}.json'); time.sleep(1)

# === Ключевые линии (полный список 163) ===
get(f'{BASE}/api/discussions/194758?page[near]=999999', f'discussion_194758_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196452?page[near]=999999', f'discussion_196452_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196488?page[near]=999999', f'discussion_196488_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196480?page[near]=999999', f'discussion_196480_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196511?page[near]=999999', f'discussion_196511_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196524?page[near]=999999', f'discussion_196524_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196475?page[near]=999999', f'discussion_196475_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196411?page[near]=999999', f'discussion_196411_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/posts?filter[discussion]=196411&page[size]=20&page[offset]=0', f'postsindex_196411_off0_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/posts?filter[discussion]=196411&page[size]=20&page[offset]=20', f'postsindex_196411_off20_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/posts?filter[discussion]=196411&page[size]=20&page[offset]=40', f'postsindex_196411_off40_{TS}.json'); time.sleep(1)
# GG-якоря: #69 (195574), #387 (195660), #48 (196411), Санити #14590/#14591 одним снапом
get(f'{BASE}/api/discussions/195574?page[near]=69', f'discussion_195574_near69_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/195660?page[near]=381', f'discussion_195660_near381_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196411?page[near]=48', f'discussion_196411_near48_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/159759?page[near]=14590', f'discussion_159759_near14590_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196424?page[near]=999999', f'discussion_196424_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196425?page[near]=999999', f'discussion_196425_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196461?page[near]=999999', f'discussion_196461_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196435?page[near]=999999', f'discussion_196435_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196428?page[near]=999999', f'discussion_196428_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196078?page[near]=999999', f'discussion_196078_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196062?page[near]=999999', f'discussion_196062_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196315?page[near]=999999', f'discussion_196315_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196415?page[near]=999999', f'discussion_196415_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196283?page[near]=999999', f'discussion_196283_near999999_{TS}.json'); time.sleep(1)
# Вырез-зона 196852: near1 для контроля зоны #8-#10 (прецедент «пинг→снос»)
get(f'{BASE}/api/discussions/196852?page[near]=1', f'discussion_196852_near1_{TS}.json'); time.sleep(1)

# === Watch-list/аномалии из №206 + тех-кластер + сага ===
WATCH = [196872, 196871, 196855, 196867, 196865, 196864, 196862, 196838, 196856, 196854,
         196846, 196777, 196817, 196832, 196842, 196836, 196843, 196851, 196853, 196857,
         196844, 196839, 196861, 196828, 196814, 196802, 196829, 196830, 196837, 196806,
         196772, 196810, 196822, 191642, 196733, 196796, 112917, 191614, 187993,
         196707, 196717, 196840, 196841, 196860, 196873, 196874, 196875, 196877, 196879, 193924, 196852, 196887, 196888, 196890, 196891, 196893, 196834, 196894, 196876, 196883, 196895, 196896, 196898]
for t in WATCH:
    get(f'{BASE}/api/discussions/{t}?page[near]=999999', f'discussion_{t}_near999999_{TS}.json'); time.sleep(1)
# Сага: #381 195192 жив? + хвост 195660 (зона #415)
get(f'{BASE}/api/discussions/195192?page[near]=381', f'discussion_195192_near381_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/195660?page[near]=430', f'discussion_195660_near430_{TS}.json'); time.sleep(1)

# === ФАЗА 2: NEW-детекция + Crios-скан + LPN-дельты ===
KNOWN = {196452, 196488, 196480, 196411, 196428, 196078, 196062, 196315, 196415, 196283,
         196424, 196461, 196490, 196511, 196469, 196474, 196475, 188595, 196326, 195079,
         195660, 195574, 195773, 196497, 196505, 196506, 196509, 196501, 196500, 196498,
         196514, 196513, 196435, 196434, 196510, 196516, 196519, 196520, 196499,
         196522, 196523, 196524, 196525, 196521, 196526, 196527, 196528, 196518,
         196529, 196530, 196531, 196496, 196260, 196100, 196258, 196532, 196536, 196533, 196537, 196539,
         196425, 196551, 196541, 196542, 196543, 196552, 196557, 196559, 196548, 196560, 196561, 196563, 196558, 196567, 196562, 196570, 196568, 196576, 196575, 196574, 196572, 196556, 196578, 196544, 196577, 196582, 196573, 196569, 196585, 196584, 196583, 196581, 196586, 196593, 196592, 196571, 196605, 196596, 196626, 196627, 196620,
         196621, 196630, 196637, 196638, 196639, 196640, 196641, 196642, 196643, 196644,
         196646, 193777, 196564, 196588, 196610, 196611, 196612, 196618, 187993, 196623,
         196624, 196625, 196628, 196629, 196631, 196633, 196634, 196635, 196150, 174335,
         185811, 196427, 196223, 195082, 196652, 196650, 196655, 196613, 196653, 196657,
         196658, 196661, 196656, 196665, 196667, 196668, 196666, 196321, 196439, 196669, 196670, 196673, 196677, 196679, 196647, 196678, 196681, 196682, 196683, 196684, 196685, 196686, 196651, 196688, 196689, 196660, 196690, 196691, 196692, 196697, 196698, 196699, 196700, 196701, 196703, 196704, 196702, 196706, 196707, 196708, 196709, 196705, 196714, 196715, 196716, 196717, 196718, 196727, 196730, 196731, 196732, 196733, 196734, 196735, 196736, 196737, 196724, 196739, 196742, 196745, 196747, 196750, 196748, 196749, 196719, 196752, 196754, 196757, 196760, 196756, 196729, 196763, 196762, 196755, 196758, 196764, 196765, 196761, 196766, 196767, 196768, 196770, 196771, 196777, 196773, 196772, 196782, 196781, 196778, 196784, 196785, 196783, 196786, 196787, 196791, 196794, 196788, 196369, 174560, 196795, 196797, 196796, 196801, 196799, 196803, 196804, 196805, 196808, 196809, 196810, 196811, 196813, 196815, 196816, 196817, 196812, 196819, 196807, 196820, 196821, 196823, 196822, 196824, 196827, 196826, 196828, 196814, 196802, 196829, 196806, 196832, 196830, 196837, 196838, 196836, 196839, 196840, 196841, 196842, 196844, 196846, 196851, 196853, 196854, 196843, 196856, 196857, 196860, 196861, 196862,
         196863, 196855, 196864, 196865, 196866, 196867, 196868, 196869, 196870, 196871, 196872, 196873, 196874, 196875, 196877, 196879, 193924, 196852, 196834, 196887, 196888, 196890, 196891, 196893, 196894, 196876, 196883, 196895, 196896, 196898}

print('\n===== NEWS TAG INDEX (off0) =====')
news = disc_items(f'tagnews_off0_{TS}.json')
seen = set()
for i in news:
    a = i.get('attributes', {})
    did = i.get('id')
    if did in seen: continue
    seen.add(did)
    try: didn = int(did)
    except Exception: didn = -1
    mark = ' [NEW]' if (didn not in KNOWN and didn > 196400) else ''
    if a.get('lastPostedAt','') >= '2026-10-16' or mark:
        print(f"  [{did}] {a.get('lastPostedAt','?')[:16]} cc={a.get('commentCount')} :: {a.get('title','')[:88]}{mark}")

print(f'\n===== FRONT INDEX (off0) — окно >= {WIN} + NEW =====')
front = disc_items(f'frontindex_off0_{TS}.json')
seen2 = set()
new_front = []
for i in front:
    a = i.get('attributes', {})
    did = i.get('id')
    if did in seen2: continue
    seen2.add(did)
    try: didn = int(did)
    except Exception: didn = -1
    mark = ' [NEW]' if (didn not in KNOWN and didn > 196400) else ''
    if mark: new_front.append(didn)
    if a.get('lastPostedAt','') >= WIN or mark:
        print(f"  [{did}] {a.get('lastPostedAt','?')[:16]} cc={a.get('commentCount')} :: {a.get('title','')[:80]}{mark}")
print(f'>>> NEW front threads: {new_front}')
for t in new_front:
    get(f'{BASE}/api/discussions/{t}?page[near]=1', f'discussion_{t}_near1_{TS}.json'); time.sleep(1)
    get(f'{BASE}/api/discussions/{t}?page[near]=999999', f'discussion_{t}_near999999_{TS}.json'); time.sleep(1)

print('\n===== SEARCH «легенда» =====')
try:
    _sl = json.load(open(os.path.join(OUT, f'search_legenda_{TS}.json')))
    for _i in (_sl.get('data') or [])[:10]:
        _ia = _i.get('attributes', {})
        print(f"  [{_i.get('id')}] cc={_ia.get('commentCount')} last={_ia.get('lastPostedAt','?')[:16]} :: {_ia.get('title','')[:80]}")
except Exception as _e:
    print(f'search parse fail: {_e}')

print('\n===== LPN/CC ДЕЛЬТЫ vs prev_lpn_174 (база 12:30, окно 1 ч) =====')
try:
    prev = json.load(open('/tmp/prev_lpn_174.json'))
    print(f'(база prev_lpn_174: {len(prev)} ключей, 12:30 UTC — +196896/+196898)')
except Exception:
    prev = {}
cur_lpn = {}
for fn in os.listdir(OUT):
    m = re.match(r'discussion_(\d+)_near999999_' + TS + r'\.json', fn)
    if not m: continue
    try:
        dd = json.load(open(os.path.join(OUT, fn)))
        aa = dd.get('data', {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
        tid = int(m.group(1))
        cur_lpn[tid] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception:
        pass
deltas = []
for tid, cur in sorted(cur_lpn.items()):
    p = prev.get(str(tid)) or prev.get(tid)
    if isinstance(p, int):
        p = {'lpn': p, 'cc': None}
    if p and (p.get('lpn') != cur['lpn'] or p.get('cc') != cur['cc']):
        deltas.append((tid, p.get('lpn'), p.get('cc'), cur['lpn'], cur['cc']))
    if not p:
        print(f'  [ЛИН/НЕТ В PREV] {tid}: lpn={cur["lpn"]} cc={cur["cc"]}')
for tid, pl, pc, cl, cc2 in deltas:
    print(f'  [{tid}] LPN {pl}->{cl} | cc {pc}->{cc2}')
json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_175.json', 'w'))
print(f'>>> prev_lpn_175.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')

print(f'\n===== CRIOS-СКАН {WIN}+ по всем снапам раунда =====')
for fn in sorted(os.listdir(OUT)):
    if not fn.endswith(f'_{TS}.json') or not fn.startswith('discussion_'): continue
    try:
        d = json.load(open(os.path.join(OUT, fn)))
    except Exception:
        continue
    inc = d.get('included', [])
    users = {u['id']: u['attributes'].get('username') for u in inc if u.get('type') == 'users'}
    for p in inc:
        if p.get('type') == 'posts':
            a = p.get('attributes', {})
            uid = p.get('relationships', {}).get('user', {}).get('data', {}).get('id')
            if users.get(uid) == 'Crios' and (a.get('createdAt') or '') >= WIN:
                print(f"  {fn[:40]}: #{a.get('number')} {a.get('createdAt')} :: {head_text(p, 150)}")

print('\n===== КЛЮЧЕВЫЕ РЕЗЮМЕ =====')
thread_summary(196872)
thread_summary(196855)
thread_summary(196867)
thread_summary(196865)
thread_summary(196838)
thread_summary(196856)
thread_summary(196854)
thread_summary(196862)
thread_summary(196452)
thread_summary(196411)
thread_summary(196488)
thread_summary(196480)
thread_summary(196511)
thread_summary(196424)
thread_summary(196425)
thread_summary(191642)
thread_summary(196806)
thread_summary(196810)
thread_summary(196846)
thread_summary(196861)
thread_summary(196873)
thread_summary(196874)
thread_summary(196875)
thread_summary(196877)
thread_summary(196879)
thread_summary(196852)
thread_summary(193924)
thread_summary(196887)
thread_summary(196888)
thread_summary(196890)
thread_summary(196891)
thread_summary(196893)
thread_summary(196894)
thread_summary(196876)
thread_summary(196883)
thread_summary(196895)
thread_summary(196896)
thread_summary(196898)
print('\n===== КАНОН #48 196411 =====')
import hashlib as _h
for off in (0, 20, 40):
    fn = f'postsindex_196411_off{off}_{TS}.json'
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        for p in d.get('data', []):
            if p.get('type') == 'posts' and p.get('attributes', {}).get('number') == 48:
                h = _h.sha256((p['attributes'].get('contentHtml') or '').encode()).hexdigest()
                print(f'  off{off}: #48 sha256={h[:16]}... match={h == CANON48}')
    except Exception as e:
        print(f'  off{off} fail: {e}')
print('\n===== GG-ЯКОРЯ =====')
for fn, want in [(f'discussion_159759_near14590_{TS}.json', [14590, 14591]),
                 (f'discussion_195574_near69_{TS}.json', [69]),
                 (f'discussion_195660_near381_{TS}.json', [387]),
                 (f'discussion_196411_near48_{TS}.json', [48])]:
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        inc = d.get('included', [])
        for p in inc:
            if p.get('type') == 'posts' and p.get('attributes', {}).get('number') in want:
                a = p.get('attributes', {})
                print(f"  {fn[11:30]}: #{a['number']} hidden={a.get('isHidden')} :: {head_text(p, 60)}")
    except Exception as e:
        print(f'  {fn}: fail {e}')
print('\n===== САГА: 195192 #381 / 195660 #387+#415-зона =====')
try:
    d = json.load(open(os.path.join(OUT, f'discussion_195192_near381_{TS}.json')))
    inc = d.get('included', [])
    nums = [p['attributes']['number'] for p in inc if p.get('type') == 'posts' and p.get('attributes', {}).get('number')]
    print(f'  195192: 381 alive={381 in nums}; cc={d["data"]["attributes"].get("commentCount")} LPN={d["data"]["attributes"].get("lastPostNumber")}')
except Exception as e:
    print(f'  195192 fail: {e}')
try:
    d = json.load(open(os.path.join(OUT, f'discussion_195660_near430_{TS}.json')))
    inc = d.get('included', [])
    nums = sorted(p['attributes']['number'] for p in inc if p.get('type') == 'posts' and p.get('attributes', {}).get('number'))
    miss = [i for i in range(min(nums), max(nums)+1) if i not in nums]
    print(f'  195660 tail: {min(nums)}..{max(nums)} гэпы={miss} (415 стабилен?)')
except Exception as e:
    print(f'  195660 fail: {e}')
print('\n===== ВЫРЕЗ-КОНТРОЛЬ 196852 (зона #8-#10) =====')
try:
    d = json.load(open(os.path.join(OUT, f'discussion_196852_near1_{TS}.json')))
    inc = d.get('included', [])
    nums = sorted(p['attributes']['number'] for p in inc if p.get('type') == 'posts' and p.get('attributes', {}).get('number'))
    miss = [i for i in range(min(nums), max(nums)+1) if i not in nums]
    print(f'  196852 near1: {min(nums)}..{max(nums)} гэпы={miss}')
except Exception as e:
    print(f'  196852 near1 fail: {e}')
print('\nDONE 54-174 PHASE1+2')
