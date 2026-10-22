# rescan54_162_fetch.py — Task 54-162: часовой cron-раунд ~19:28 UTC 22.10 (22:28 МСК) —
# ШТАТНЫЙ час после 54-161 (18:28-18:5x UTC, ledger №202; окно дельт 18:30..19:30) и
# межраунда 54-161-B (PAT-restore: push-канал восстановлен, оба ремоута на 2511236e).
# Контекст и watch-list из №202:
# (1) ★★ ТЕХ-КЛАСТЕР 17:44-18:35: 196864 «Крашит игру» (OP MisterKybik, cc=6, ищет логи крашей)
# + 196865 «Несчастье за несчастьем. Реорганизация 😔» (OP Wichspid, cc=20/LPN=20 за 50 мин —
# наезд на кадровую тему; Shmendergar #19 18:40 подтвердил на чистой системе; _Meliodas_
# защищает «30.09 быстро пофиксили + компенса»; Med0nt «перезатачивается под другой движок»)
# + 196867 «А что с серверами?» (OP DOOMKNIGHT, cc=7, пинг 13→50-70, «@Рупоры»)
# + 196870 «Это не я)» (OP OlderS, мем). ОФИЦ. ОТВЕТА НЕТ. Продолжение? Ответ? Новые тех-треды?
# (2) ★ 191642 «разрабы забыли реранить обвесы?» РАЗГОН 294→313 (+19/час УСКОРЕНИЕ):
# Shmendergar #310 18:26 ПИНГ @Crios («фамас отставал из-за невозможности въебать дистонию»),
# Bi1ly #311/#312 «не трогайте мою дистонию ТВАРИ», Ambercleaved #313. Crios ответит на пинг?
# (3) ★ CRIOS 9-Й ЧАС ОФИЦ.: 196772 #42 18:07 «ждите обновление системы распределения» (тиры) —
# 6-й офиц. за 2.5 ч; РЕЙТИ-ГНЕВ ИГНОР: 196862 ЗАМОРОЗКА на 18 (#18 17:19, 90+ мин),
# KM_XEROX пинг (196856) без ответа, записки СТОП 3.5+ ч, Санити СТОП 29 ч (#14610).
# (4) ★ 196854 jlococen-диалог: OP Leverset97 #69/#70 18:27 «Получится что-нибуть сделать?» —
# мод молчит после #67; 196856 ВЫРЕЗ №3 (LPN=42 cc=40); 196846 +8 35 (ганпорно-дискуссия +
# kravv285 «за это банят» + ego_fanak мета-юмор про сносы); 196777 ФЛЕЙМ-ВОЛНА blackfoxstalker
# ×5 за 6 мин + kravv285 #73 «иди нахуй»; 196810 29-Й ЧАС БЕЗ офиц. (88); Арена 8-Й ЧАС (32,
# награды-гнев stm #30 «наград 0»); чистки 196752/196778/196805 ВСЕ СТОП 5-Й ЧАС; 196411 34-Й
# ЧАС канона ×2 OK (гэпы [15,33,63-78,88]); NEW-окно ПУСТО; ТГК 3227 НЕТ 3-Й ЧАС; Спектрум
# 7954 rx ❤53/5.25K РОСТ 4-Й ЧАС (7955 НЕТ); 404: 196707/196717 70-Й + 196840/196841 6-Й +
# 196860 3-Й; 196796 возврат 25-Й ЧАС; search «легенда» OK после фикс-парса.
# Уроки: near1+near999999 ОБА для NEW; LPN и cc сверять РАЗДЕЛЬНО (вырезы); /tmp НЕ персистентен;
# GG-якоря #14590/#14591 брать near=14590 одним снапом (могут выпасть из near999999-окна).
import json, os, urllib.request, time, hashlib, re

TS = '20261022_1930'  # фиксированный TS раунда 54-162 (SKIP-доборы переиспользуют файлы)
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
CANON48 = 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e'

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

# === ФАЗА 1: витрина новостей + фронт + ТГК + search ===
get(f'{BASE}/api/discussions?filter[tag]=news&sort=-lastPostedAt&page[size]=50&page[offset]=0', f'tagnews_off0_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions?page[offset]=0', f'frontindex_off0_{TS}.json'); time.sleep(1)
get('https://t.me/s/stalzone', f'tg_stalzone_page0_{TS}.html', validate_json=False); time.sleep(1)
get('https://t.me/s/spectrum_zone', f'tg_spectrum_page0_{TS}.html', validate_json=False); time.sleep(1)
get(f'{BASE}/api/discussions?filter[q]=%D0%BB%D0%B5%D0%B3%D0%B5%D0%BD%D0%B4%D0%B0&page[offset]=0', f'search_legenda_{TS}.json'); time.sleep(1)

# === Ключевые линии ===
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
# GG-якоря (54-135b): #69 (195574), #387 (195660), #48 (196411), Санити #14590/#14591 near=14590 одним снапом
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

# === РЕЗЮМЕ ===
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
         196863, 196864, 196865, 196866, 196867, 196868, 196869, 196870}

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

print('\n===== FRONT INDEX (off0) — только живое/новое (окно >= 18:30) =====')
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
    if a.get('lastPostedAt','') >= '2026-10-22T18:30' or mark:
        print(f"  [{did}] {a.get('lastPostedAt','?')[:16]} cc={a.get('commentCount')} :: {a.get('title','')[:80]}{mark}")
print(f'>>> NEW front threads (auto OP-fetch phase 2 в конце): {new_front}')

print('\n===== SEARCH «легенда» =====')
try:
    _sl = json.load(open(os.path.join(OUT, f'search_legenda_{TS}.json')))
    for _i in (_sl.get('data') or [])[:10]:
        _ia = _i.get('attributes', {})
        print(f"  [{_i.get('id')}] cc={_ia.get('commentCount')} last={_ia.get('lastPostedAt','?')[:16]} :: {_ia.get('title','')[:80]}")
except Exception as _e:
    print(f'search parse fail: {_e}')

print('\n===== 194758 «Новый раздел для легенд» =====')
thread_summary(194758)
print('\n===== 196452 Талоны PvE (~214 ч офиц. молчания, флешмоб талонов 84-Й ЧАС?) =====')
thread_summary(196452)
print('\n===== 196511 Хотфикс (8-е сутки с 19:34 UTC 15.10; чейнджлога нет) =====')
thread_summary(196511)
print('\n===== 196488 Кейс =====')
thread_summary(196488)
print('\n===== 196480 Кейс-шансы (Crios-тишина в кейсе ~125 ч) =====')
thread_summary(196480)

print('\n===== 196411 / #48 канон + union-карта (гэпы [15,33,63-78,88]; сносов нет 35-Й ЧАС?) =====')
p411 = thread_summary(196411)
union = set()
for off in ('off0', 'off20', 'off40'):
    for p in posts_of(f'postsindex_196411_{off}_{TS}.json'):
        union.add(p.get('attributes', {}).get('number'))
for p in p411:
    union.add(p.get('attributes', {}).get('number'))
nums = sorted(n for n in union if n)
gaps = sorted(set(range(1, nums[-1] + 1)) - set(nums))
print(f'>>> union 196411 = 1..{nums[-1]}, гэпы: {gaps}')
for off in ('off20', 'off40'):
    fn = os.path.join(OUT, f'postsindex_196411_{off}_{TS}.json')
    try:
        d = json.load(open(fn))
        for i in (d.get('data') or []) + (d.get('included') or []):
            if isinstance(i, dict) and i.get('type') == 'posts' and i.get('attributes', {}).get('number') == 48:
                h = hashlib.sha256((i['attributes'].get('contentHtml') or '').encode()).hexdigest()
                print(f">>> #48 ({off}): sha256 {h[:16]}... {'CANON OK' if h == CANON48 else '!!! ИЗМЕНИЛСЯ'} rx={sum((i['attributes'].get('reactionCounts') or {}).values())}")
    except Exception as e:
        print(f'#48 {off} fail: {e}')

print('\n===== 196424 ОТС (итоги 94+ ч НЕ ВЫШЛИ) / 196425 фидбек =====')
thread_summary(196424)
thread_summary(196425)
print('\n===== 196461 Раздутый ттк / 196435 Колизей-калибровка / 196428 / 196078 / 196062 / контролы 196315/196415/196283 =====')
thread_summary(196461)
thread_summary(196435)
thread_summary(196428)
thread_summary(196078)
thread_summary(196062)
for tid in (196315, 196415, 196283):
    pp = posts_of(f'discussion_{tid}_near999999_{TS}.json')
    try:
        dd = json.load(open(os.path.join(OUT, f'discussion_{tid}_near999999_{TS}.json')))
        aa = dd.get('data', {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
        nums2 = sorted((p.get('attributes', {}).get('number') or 0) for p in pp)
        last = max((p.get('attributes', {}).get('createdAt') or '' for p in pp), default='')
        print(f"[{tid}] cc={aa.get('commentCount')} lastPostNumber={aa.get('lastPostNumber')} lastCreatedAt={last[:16]} tail={nums2[-3:] if nums2 else []}")
    except Exception as e:
        print(f'[{tid}] attrs fail {e}')

print('\n===== ТГК stalzone page0 (3227+? — 3226 «Суматоха в Баре» последний 15:00, 4-Й ЧАС тишины) =====')
try:
    html = open(os.path.join(OUT, f'tg_stalzone_page0_{TS}.html'), encoding='utf-8', errors='ignore').read()
    msgs = []
    for m in re.finditer(r'data-post="stalzone/(\d+)"[\s\S]*?<time datetime="([^"]+)"[\s\S]*?(?:<div class="tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>)?[\s\S]*?(?=data-post="stalzone/|</section>)', html):
        mid, ts, txt = m.group(1), m.group(2), m.group(3) or ''
        txt = re.sub(r'<br/?>', ' ', txt)
        txt = re.sub(r'<[^>]+>', '', txt)
        txt = re.sub(r'\s+', ' ', txt).strip()
        msgs.append((int(mid), ts[:16], txt))
    for mid, ts, txt in msgs[-6:]:
        print(f'  [{mid}] {ts} :: {txt[:110]}')
except Exception as e:
    print(f'TG parse fail: {e}')

print('\n===== ТГК Спектрума spectrum_zone page0 (7955+? 7954 rx ❤53 РОСТ 4-Й ЧАС) =====')
try:
    html2 = open(os.path.join(OUT, f'tg_spectrum_page0_{TS}.html'), encoding='utf-8', errors='ignore').read()
    msgs2 = []
    for m in re.finditer(r'data-post="spectrum_zone/(\d+)"[\s\S]*?<time datetime="([^"]+)"[\s\S]*?(?:<div class="tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>)?[\s\S]*?(?=data-post="spectrum_zone/|</section>)', html2):
        mid2, ts2, txt2 = m.group(1), m.group(2), m.group(3) or ''
        txt2 = re.sub(r'<br/?>', ' ', txt2)
        txt2 = re.sub(r'<[^>]+>', '', txt2)
        txt2 = re.sub(r'\s+', ' ', txt2).strip()
        msgs2.append((int(mid2), ts2[:16], txt2))
    for mid2, ts2, txt2 in msgs2[-8:]:
        print(f'  [{mid2}] {ts2} :: {txt2[:130]}')
except Exception as e:
    print(f'TG-SPEC parse fail: {e}')

# === Хвосты окна 54-162 (дельты 18:30..19:30): watch-list из №202 ===
WATCH = [159759, 196862, 191642, 196864, 196865, 196867, 196870, 196772, 196854, 196856,
         196846, 196777, 196799, 196810, 196838, 196842, 196832, 196836, 196843, 196851,
         196839, 196853, 196857, 196844, 196861, 196828, 196814, 196802, 196829, 196806,
         196830, 196837, 196827, 196826, 196824, 196822, 196820, 196823, 196821, 196807,
         196819, 196803, 196804, 196805, 196808, 196809, 196811, 196812, 196813, 196815,
         196816, 196817, 196796, 196801, 196795, 196797, 196791, 196794, 196788, 196778,
         196784, 196785, 196783, 196786, 196787, 196772, 196782, 196781, 196773, 196771,
         196770, 196768, 196767, 196766, 196757, 196764, 196765, 196761, 196763, 196762,
         196755, 196758, 196760, 196756, 196754, 196752, 196750, 196749, 196748, 196747,
         196745, 196739, 196742, 196737, 196734, 196735, 196736, 196732, 196733, 196730,
         196731, 196727, 196725, 196724, 196722, 196721, 196720, 196718, 196655, 196705,
         196714, 196715, 196716, 196702, 196706, 196709, 196708, 196701, 196704, 196703,
         196692, 196688, 196699, 196700, 196698, 196689, 196667, 196697, 196686, 196548,
         195080, 195081, 195083, 196690, 196646, 196661, 196621, 196108, 196673, 196641,
         196627, 196678, 196501, 196668, 196681, 196643, 196684, 196683, 196682, 196665,
         196658, 196679, 196626, 179952, 196677, 195249, 196669, 180244, 196610, 196439,
         196321, 196657, 196620, 196653, 196652, 196650, 196613, 196640, 196644, 196638,
         196561, 193777, 185811, 196630, 196624, 196623, 196631, 196633, 196634, 196564,
         196635, 196588, 196427, 196637, 196639, 196625, 196629, 196150, 174335, 196612,
         196618, 196611, 187993, 196572, 196434, 196382, 179857, 195082, 196223, 191614, 112917,
         # 404-контроли: 196707/196717 (71-Й ЧАС), 196840/196841 (снос 7-Й ЧАС), 196860 (снос 4-Й ЧАС)
         196707, 196717, 196840, 196841, 196860]
_seenw = set()
for tid in WATCH:
    if tid in _seenw: continue
    _seenw.add(tid)
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)
    thread_summary(tid, near='999999')

print('\n===== GETGOOD-ДЕЛЬТА (база 54-160/161: ВСЕ 5 СТАБИЛЬНО 19-Й ЧАС; РАЗМОРОЗКА = СИНХРОН по всем 5): #69 likes=1 rx{34:6}, #387 likes=1 rx{35:1}, #48 likes=2, #14590 likes=2 rx{33:3}, #14591 likes=1 rx{33:1} =====')
def anchor_like(tid, near, pnum, base_likes, base_rx):
    fn = f'discussion_{tid}_near{near}_{TS}.json'
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        items = d.get('data') if isinstance(d.get('data'), list) else []
        for i in items + (d.get('included') or []):
            if isinstance(i, dict) and i.get('type') == 'posts' and (i.get('attributes', {}) or {}).get('number') == pnum:
                a = i.get('attributes', {}) or {}
                rc = {k: v for k, v in (a.get('reactionCounts') or {}).items() if v}
                delta = (a.get('likesCount') != base_likes) or (rc != base_rx)
                print(f'  [anchor d/{tid} #{pnum}] likes={a.get("likesCount")} rx={rc} :: ' + ('ДЕЛЬТА!' if delta else 'стабильно'))
                return
        print(f'  [anchor d/{tid} #{pnum}] НЕ НАЙДЕН в окне near={near}')
    except Exception as e:
        print(f'  [anchor d/{tid} #{pnum}] fail: {e}')
anchor_like(195574, 69, 69, 1, {'34': 6})
anchor_like(195660, 381, 387, 1, {'35': 1})
anchor_like(196411, 48, 48, 2, {})
anchor_like(159759, 14590, 14590, 2, {'33': 3})
anchor_like(159759, 14590, 14591, 1, {'33': 1})

print('\n===== RANKS (OP-группы watch-тредов + тех-кластер) =====')
def op_rank(tid, near='999999'):
    try:
        d = json.load(open(os.path.join(OUT, f'discussion_{tid}_near{near}_{TS}.json')))
        groups = {i['id']: (i.get('attributes', {}) or {}).get('nameSingular') for i in (d.get('included') or []) if i.get('type') == 'groups'}
        users = {i['id']: i for i in (d.get('included') or []) if i.get('type') == 'users'}
        opid = ((d.get('data') or {}).get('relationships', {}) or {}).get('user', {}).get('data', {})
        opid = opid.get('id') if isinstance(opid, dict) else None
        u = users.get(opid) or {}
        a = u.get('attributes', {})
        gids = [x.get('id') for x in u.get('relationships', {}).get('groups', {}).get('data', [])]
        print(f"[rank {tid}] OP={a.get('username')} groups={[groups.get(g, g) for g in gids]} join={(a.get('joinTime') or '?')[:10]} cc={a.get('commentCount')} warnings={a.get('visibleWarningCount')}")
    except Exception as e:
        print(f'[rank {tid}] fail: {e}')
for _rt in (196864, 196865, 196867, 196870, 196862, 191642, 196854, 196856, 196846, 196777, 196799, 196810, 196838, 196842, 196832, 196836, 196843, 196851, 196839, 196772, 196828, 196844, 196857, 196853, 196861, 196829, 196806, 196805, 196796, 196803):
    op_rank(_rt)

# === FAST-RULE: середина для быстрорастущих (>15/час); PREV_LPN из /tmp/prev_lpn_162.json (105 ключей, база №202) ===
PREV_LPN = {}
try:
    PREV_LPN = {int(k): v for k, v in json.load(open('/tmp/prev_lpn_162.json')).items()}
    print(f'PREV_LPN loaded: {len(PREV_LPN)} keys')
except Exception as e:
    print(f'PREV_LPN LOAD FAIL: {e}')
print('\n===== FAST-RULE =====')
for _tid, _plpn in sorted(PREV_LPN.items()):
    try:
        _dd = json.load(open(os.path.join(OUT, f'discussion_{_tid}_near999999_{TS}.json')))
        _aa = _dd.get('data', {}).get('attributes', {}) if isinstance(_dd.get('data'), dict) else {}
        _lpn = _aa.get('lastPostNumber') or 0
        _delta = _lpn - _plpn
        if _delta > 15:
            _mid = (_plpn + _lpn) // 2
            get(f'{BASE}/api/discussions/{_tid}?page[near]={_mid}', f'discussion_{_tid}_near{_mid}_{TS}.json'); time.sleep(1)
            print(f'[fast-rule] {_tid}: LPN {_plpn}->{_lpn} (delta {_delta}) -> middle near={_mid}')
        else:
            print(f'[fast-rule] {_tid}: LPN {_plpn}->{_lpn} (delta {_delta}) <=15')
    except Exception as _e:
        print(f'[fast-rule] {_tid} fail ({_e}) — 404?')

print('\n===== БОЛЬШИЕ ТРЕДЫ (cc из front-атрибутов) =====')
for i in front:
    if str(i.get('id')) in ('112917', '164665', '167367', '186525', '187993'):
        a = i.get('attributes', {})
        print(f"  [{i.get('id')}] cc={a.get('commentCount')} last={a.get('lastPostedAt','?')[:16]} :: {a.get('title','')[:60]}")

# === ФАЗА 2: NEW-треды фронта — OP near=1 (урок: OP умирает вместе с тредом) ===
if new_front:
    print('\n===== ФАЗА 2: NEW OP (near=1) =====')
    for _nf in new_front:
        get(f'{BASE}/api/discussions/{_nf}?page[near]=1', f'discussion_{_nf}_near1_{TS}.json'); time.sleep(1)
        thread_summary(_nf, near='1')
        op_rank(_nf, near='1')

# === СОХРАНЕНИЕ PREV_LPN для 54-163 ===
NEWPREV = {}
for _tid, _plpn in PREV_LPN.items():
    NEWPREV[str(_tid)] = _plpn
for _fn in os.listdir(OUT):
    if not _fn.endswith(f'_{TS}.json') or not _fn.startswith('discussion_'):
        continue
    _tid = _fn.split('_')[1]
    try:
        _d2 = json.load(open(os.path.join(OUT, _fn)))
        _a2 = _d2.get('data', {}).get('attributes', {}) if isinstance(_d2.get('data'), dict) else {}
        _l2 = _a2.get('lastPostNumber')
        if _l2:
            NEWPREV[str(_tid)] = max(NEWPREV.get(str(_tid), 0), _l2)
    except Exception:
        pass
try:
    json.dump(NEWPREV, open('/tmp/prev_lpn_163.json', 'w'), ensure_ascii=False, indent=0)
    print(f'\nPREV_LPN saved: /tmp/prev_lpn_163.json ({len(NEWPREV)} keys)')
except Exception as e:
    print(f'PREV_LPN SAVE FAIL: {e}')

print(f'\nTS={TS}')
