# rescan54_123_fetch.py — Task 54-123: часовой cron-раунд ~04:30 UTC 21.10 (07:30 МСК 21.10).
# База = 54-122 (03:55 UTC, acb090b; обе репы = acb090b, тридцать первый подряд
# полный зелёный цикл). creds/vault/bundle на месте — ТОКЕН ПО-ПРЕЖНЕМУ НЕ РОТИРОВАН (5-е
# напоминание автору: живой ghp_ с 18.10 на публичной MEGA-ссылке, чистки не решают).
# УРОКИ 54-113..122: обход делить сразу (foreground timeout 585с + sed-finisher с фикс. TS
# и родным SKIP); фоновые запуски (nohup И setsid) среда убивает молча; при R9b (замена
# головы кортежа) ПРОВЕРЯТЬ, что старая голова не теряется — 196757 удержан с 54-115,
# 196768/196767/196766/196770/196771 удержаны; шапка заменяется ЦЕЛИКОМ по якорю «import json»
# (7 раундов без сбоев); НОЧЬ 54-119..122: run1 стабильно не укладывается в 585с —
# sed-finisher (TS фикс.) сразу после run1, 1-2 добора до EXIT=0.
# УРОК 54-122: R10 обновлять PREV_LPN по ВСЕМ замерам ledger прошлого раунда, а не только
# по fast-rule-хитам (иначе fast-rule считает от устаревшего PREV — ложные срабатывания).
# ВНИМАНИЕ: ТЕХРАБОТЫ СЕГОДНЯ СРЕДА 21.10 9:00-11:30 МСК (06:00-08:30 UTC) — ПОДТВЕРЖДЕНЫ
# АВТОРОМ (54-117b): 54-126/54-127 (06:27/07:27 UTC) — ожидаем «round skipped» (штатно,
# не чинить; пробный get() форума первым шагом); 54-128 (08:27 UTC) пограничный; 54-123
# штатный (за 1.5 ч до окна); 54-124 (05:27 UTC) последний перед окном.
# Блок fast-rule в конце («БЫСТРЫЙ ТРЕД — ТРИ СЛЕПКА»): при delta LPN >15/час добирается
# середина; PREV_LPN={195081:1076, 196718:115, 196721:18, 196727:38, 196730:32,
# 196732:27, 196734:53, 196735:38, 196739:13, 196742:13, 196745:14, 196747:4,
# 196748:32, 196749:18, 196750:13, 196752:19, 196754:11, 196757:1, 196760:32, 196756:23,
# 196763:32, 196762:2, 196755:33, 196758:21, 196764:7, 196765:8, 196761:18, 196766:1,
# 196767:5, 196768:6, 196770:65, 196771:10}.
# СЛЕДИТЬ: ИТОГИ ОТС? (196424=160 тишина 54.5+ ч; 196425=125) — час 55; 196770 бан-тред
# ЗАТУХ ОКОНЧАТЕЛЬНО? (LPN 65, +1/час — штаб EXENS так и не ответил); 196755 «вася» 4-Й
# ЧАС? (LPN 33, две волны в 3-м часу); 196771 тульпа-флейм с kravv285 3-й час? (cc=10);
# 196702 «Новое целеполагание» продолжит? (ожил после суток тишины, 41); Братство 187993
# продолжит +6/час? (1207); Кот-арбуз 191614 (7042); MAMICH 196718 (115, встал); NEW
# 54-121: 196771 «Тульпа, сигналы, Сено и фантазии» Колян_Блистер (01:37); 196770
# «Возможен ли бан по ошибке ?» AlexMrz2 (22:54 20.10); NEW 54-118: 196768 «Кал лизей»
# (6, встал); NEW 54-117: 196767 казино/покер (5, встал); NEW 54-116: 196766 фанфик (1,
# встал); NEW 54-115: 196764 анимации (7)/196765 раге (8); NEW 54-113: 196763 ИИ-тред
# (32, встал)/196762 дикий север (2)/196755 вася (33!)/196758 тикрейт (21); вчерашние
# NEW: 196760 Kvass4-драма (32)/196756 (23)/196752 «Слухи не утихают» (19)/196754 лаунчер
# (11)/196750 Коллектор (13)/196749 споты (18)/196748 Распред? (32, встал)/196747
# Илларион (4)/196739 шиз-кресты (13)/196737 баг-репорт (13)/196735 ГПТ-кейс (38)/196736
# мерч-стор (8)/196733 Derya (19)/196720 (6)/196732 (27); 196727 (38)/196730 (32)/196731
# лок (cc=6/LPN 7, ~22.5 ч); 196510 КАЛЛибровка (36/37)/196708 Оптимизация (54)/196706
# (72)/196704 (72 рюкзаки)/196702 «Новое целеполагание» (40/41, ОЖИЛ last 03:05)/196703
# (18)/196643 (56); stm: 196716 (27)/196705 (22)/196709 (22)/196701 (23/24)/196714 (15)/
# 196715 (14); NEW-старики: 196721 (18)/196724 (11)/196722 (6)/196720 (6)/196725 (4);
# 195080 рука (780/829)/195083 (176/193); 196532 Тирлист (343/344, встал); 187993
# Братство (1207); 196610 «Раздача отс» (37); фон: 194423 «Осенний сезон» (127), 191614
# Кот-арбуз (7042), 196321 рваные кадры (145), 196108 зомби (87/88); СНОСЫ 196411 36-й
# час? (#90?, LPN=89, гэпы [15,33,63-77,88]); 196501 продолжит? (158); флешмоб талонов
# 45-й час? (196452 cc=30, ~174 ч офиц. молчания); ТГК 3220? (3219@16:00, пауза ~11.5 ч);
# 404-КОНТРОЛЬ: 196707 + 196717 (31-й час).
# База №165 (03:55 UTC, TS 0331): ★★ 196770 РАЗГОН ЗАТУХАЕТ 64→65 (+1/час, last 03:26,
# пик 22:54-02:27 пройден); ★ 196755 3-Й ЧАС 24→33 (+9/час, две волны 01:46-02:16 и
# 02:48-02:55, cc=31 — 2 вырезано); ★ 196771 флейм +2 (8→10, last 03:03); ★ 196702
# «Новое целеполагание» ОЖИЛ +1 (40→41, last 03:05); ★ 187993 Братство +6 (1201→1207,
# last 02:33); ★ 191614 Кот-арбуз +1 (7042, last 03:20); ★ 112917 вайб ВЕРНУЛСЯ на front
# off0 (66429, last 02:54); 196376 «Лучший проводник» cc=41 last 03:21; ЗАТИШЬЕ: 196761
# (18)/196765 (8)/196735 (38)/196756 (23)/MAMICH 196718 (115) — все 0; ИТОГИ ОТС НЕ
# ВЫШЛИ (ЧАС 54); 196411 35-Й ЧАС БЕЗ СНОСОВ (гэпы неизменны, канон OK rx=0); ТГК 3220
# нет (~10.5 ч); флешмоб 44-Й ЧАС; Crios ~83 ч; 196511 9-е сутки; клан-жалоба 14-Й ЧАС;
# 404-контроли 31-Й ЧАС; fast-rule ×1 (196755 от устаревшего PREV 12 → near=22 добран).


import json, os, urllib.request, time, hashlib, datetime, re

TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
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
        print(f'[{tid}] attrs fail {e}')
    tail = sorted(pp, key=lambda p: p.get('attributes', {}).get('number') or 0)[-6:]
    for p in tail:
        a = p.get('attributes', {})
        print(f"  #{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")
    return pp

# === ФАЗА 1: витрина новостей + фронт + ТГК ===
get(f'{BASE}/api/discussions?filter[tag]=news&sort=-lastPostedAt&page[size]=50&page[offset]=0', f'tagnews_off0_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions?page[offset]=0', f'frontindex_off0_{TS}.json'); time.sleep(1)
get('https://t.me/s/stalzone', f'tg_stalzone_page0_{TS}.html', validate_json=False); time.sleep(1)

# === Ключевые линии ===
get(f'{BASE}/api/discussions/196452?page[near]=999999', f'discussion_196452_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196488?page[near]=999999', f'discussion_196488_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196480?page[near]=999999', f'discussion_196480_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196511?page[near]=999999', f'discussion_196511_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196524?page[near]=999999', f'discussion_196524_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196475?page[near]=999999', f'discussion_196475_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196521?page[near]=999999', f'discussion_196521_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196528?page[near]=999999', f'discussion_196528_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196518?page[near]=999999', f'discussion_196518_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196529?page[near]=999999', f'discussion_196529_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196530?page[near]=999999', f'discussion_196530_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196531?page[near]=999999', f'discussion_196531_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196532?page[near]=999999', f'discussion_196532_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196536?page[near]=999999', f'discussion_196536_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196533?page[near]=999999', f'discussion_196533_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196496?page[near]=999999', f'discussion_196496_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196260?page[near]=999999', f'discussion_196260_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196411?page[near]=999999', f'discussion_196411_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/posts?filter[discussion]=196411&page[size]=20&page[offset]=0', f'postsindex_196411_off0_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/posts?filter[discussion]=196411&page[size]=20&page[offset]=20', f'postsindex_196411_off20_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/posts?filter[discussion]=196411&page[size]=20&page[offset]=40', f'postsindex_196411_off40_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196424?page[near]=999999', f'discussion_196424_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196461?page[near]=999999', f'discussion_196461_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196435?page[near]=999999', f'discussion_196435_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196510?page[near]=999999', f'discussion_196510_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196520?page[near]=999999', f'discussion_196520_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196499?page[near]=999999', f'discussion_196499_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196516?page[near]=999999', f'discussion_196516_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196513?page[near]=999999', f'discussion_196513_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196522?page[near]=999999', f'discussion_196522_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196523?page[near]=999999', f'discussion_196523_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196428?page[near]=999999', f'discussion_196428_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196078?page[near]=999999', f'discussion_196078_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196062?page[near]=999999', f'discussion_196062_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196315?page[near]=999999', f'discussion_196315_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196415?page[near]=999999', f'discussion_196415_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196283?page[near]=999999', f'discussion_196283_near999999_{TS}.json'); time.sleep(1)
# --- хвосты: 196425/196552/196557 + 196537/196539 + младшие NEW 196551/196542/196543 ---
get(f'{BASE}/api/discussions/196425?page[near]=999999', f'discussion_196425_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196552?page[near]=999999', f'discussion_196552_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196557?page[near]=999999', f'discussion_196557_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196537?page[near]=999999', f'discussion_196537_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196539?page[near]=999999', f'discussion_196539_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196551?page[near]=999999', f'discussion_196551_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196542?page[near]=999999', f'discussion_196542_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196543?page[near]=999999', f'discussion_196543_near999999_{TS}.json'); time.sleep(1)

# === РЕЗЮМЕ ===
KNOWN = {196452, 196488, 196480, 196411, 196428, 196078, 196062, 196315, 196415, 196283,
         196424, 196461, 196490, 196511, 196469, 196474, 196475, 188595, 196326, 195079,
         195660, 195574, 195773, 196497, 196505, 196506, 196509, 196501, 196500, 196498,
         196514, 196513, 196435, 196434, 196510, 196516, 196519, 196520, 196499,
         196522, 196523, 196524, 196525, 196521, 196526, 196527, 196528, 196518,
         196529, 196530, 196531, 196496, 196260, 196100, 196258, 196501, 196532, 196536, 196533, 196537, 196539,
         196425, 196551, 196541, 196542, 196543, 196552, 196557, 196559, 196548, 196560, 196561, 196563, 196558, 196567, 196562, 196570, 196568, 196576, 196575, 196574, 196572, 196556, 196578, 196544, 196577, 196582, 196573, 196569, 196585, 196584, 196583, 196581, 196586, 196593, 196592, 196571, 196605, 196596, 196626, 196627, 196620,
         196621, 196630, 196637, 196638, 196639, 196640, 196641, 196642, 196643, 196644,
         196646, 193777, 196564, 196588, 196610, 196611, 196612, 196618, 187993, 196623,
         196624, 196625, 196628, 196629, 196631, 196633, 196634, 196635, 196150, 174335,
         185811, 196427, 196223, 195082, 196434, 196652, 196650, 196655, 196613, 196653, 196657,
         196658, 196661, 196656, 196665, 196667, 196668, 196666, 196321, 196439, 196669, 196670, 196673, 196677, 196679, 196647, 196678, 196681, 196682, 196683, 196684, 196685, 196686, 196651, 196688, 196689, 196660, 196690, 196691, 196692, 196697, 196698, 196699, 196700, 196701, 196703, 196704, 196702, 196706, 196707, 196708, 196709, 196705, 196714, 196715, 196716, 196717, 196718, 196727, 196730, 196731, 196732, 196733, 196734, 196735, 196736, 196737, 196724, 196739, 196742, 196745, 196747, 196750, 196748, 196749, 196719, 196752, 196754, 196757, 196760, 196756, 196729, 196763, 196762, 196755, 196758, 196764, 196765, 196761, 196766, 196767, 196768, 196770, 196771, 196369, 174560}

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

print('\n===== FRONT INDEX (off0) — только живое/новое =====')
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
    if a.get('lastPostedAt','') >= '2026-10-21T03:27' or mark:
        print(f"  [{did}] {a.get('lastPostedAt','?')[:16]} cc={a.get('commentCount')} :: {a.get('title','')[:80]}{mark}")
print(f'>>> NEW front threads to OP-fetch (phase 2): {new_front}')

print('\n===== 196452 Талоны PvE (~174 ч офиц. молчания) =====')
thread_summary(196452)

print('\n===== 196511 Хотфикс (жетоны-пропажа; был cc=31, 9-е сутки) =====')
thread_summary(196511)

print('\n===== 196488 Кейс =====')
thread_summary(196488)
print('\n===== 196480 Кейс-шансы (был cc=171; Crios-тишина ~84 ч) =====')
thread_summary(196480)

print('\n===== 196524 Глеб (был cc=1147 LOCKED) =====')
thread_summary(196524)
print('\n===== 196475 Амнистия (был cc=252) =====')
thread_summary(196475)
print('\n===== 196522 Штыриуса тред =====')
thread_summary(196522)
print('\n===== 196523 ОБРАЩЕНИЕ К EXBO =====')
thread_summary(196523)

print('\n===== 196411 / #48 канон + union-карта (гэпы [15,33,63-77,88], волна 36-й час — следим #90+) =====')
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

print('\n===== 196532 Тирлист Завозов (ожил +5, cc=343/LPN 344) =====')
thread_summary(196532)
print('\n===== 196536 Смена оружия (был cc=8) =====')
thread_summary(196536)
print('\n===== 196533 Американская гитара (был cc=2) =====')
thread_summary(196533)

print('\n===== 196537 Мастерский детектор прикопов (был cc=35) =====')
thread_summary(196537)
print('\n===== 196539 Вылеты vs Передовой кейс (был cc=30) =====')
thread_summary(196539)

print('\n===== 196424 ОТС (ЗАКРЫЛОСЬ 20:59 UTC, снят с закрепа 00:40, тишина 54.5+ ч, ИТОГИ = день 20.10, ждём; был cc=160) =====')
thread_summary(196424)
print('\n===== 196425 ОФИЦ. СБОР ФИДБЕКА ОТС (был cc=124; итоги ОТС = НЕ ВЫШЛИ 54.5+ ч) =====')
thread_summary(196425, near='999999')

print('\n===== 196461 Раздутый ттк =====')
thread_summary(196461)
print('\n===== 196435 Колизей-калибровка (был cc=154) =====')
thread_summary(196435)
print('\n===== 196510 КАЛЛибровка-2 (ожил в 54-117, cc=36/LPN 37) =====')
thread_summary(196510)
print('\n===== 196520 Колизей кодекс =====')
thread_summary(196520)
print('\n===== 196499 =====')
thread_summary(196499)
print('\n===== 196516 Соло гемлпей (был cc=22) =====')
thread_summary(196516)
print('\n===== 196513 =====')
thread_summary(196513)
print('\n===== 196531 Лишняя информация на пердметах (был cc=21) =====')
thread_summary(196531)
print('\n===== 196496 Простой пример (был cc=103, соло-флейм волна) =====')
thread_summary(196496)
print('\n===== 196260 КАНОН СТАЛЗОН (был cc=59) =====')
thread_summary(196260)
print('\n===== 196428 =====')
thread_summary(196428)
print('\n===== 196078 (магпулы) =====')
thread_summary(196078)
print('\n===== 196062 =====')
thread_summary(196062)
print('\n===== КОНТРОЛЫ 196315/196415/196283 =====')
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

print('\n===== ТГК stalzone page0 (3220? (3219@16:00 дубль анонса техработ) пауза ~11.5 ч) =====')
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

print('\n===== Хвосты окна 54-123: 196771 (тульпа-флейм 3-Й ЧАС?) + 196770 (затух? LPN 65) + 196768 + 196767 + 196766 + 196757 (УДЕРЖИВАЕТСЯ!) + 196755 (4-Й ЧАС?) + 196761 + mamich-поток 196718/196721 + NEW 54-113 196763/196762/196758 + вчерашние NEW 196760/196756/196754/196752/196750/196749/196748/196747/196745/196739/196742/196737/196734/196735/196736/196732/196733/196730/196731/196727 + stm-выжившие + 404-контроль =====')
for tid in (196771, 196770, 196768, 196767, 196766, 196757, 196764, 196765, 196761, 196763, 196762, 196755, 196758, 196760, 196756, 196754, 196752, 196750, 196749, 196748, 196747, 196745, 196739, 196742, 196737, 196734, 196735, 196736, 196732, 196733, 196730, 196731, 196727, 196725, 196724, 196722, 196721, 196720, 196718, 196655, 196705, 196714, 196715, 196716, 196717, 196702, 196706, 196709, 196707, 196708, 196701, 196704, 196703, 196692, 196688, 196699, 196700, 196698, 196689, 196667, 196697, 196686, 196548, 195080, 195081, 195083, 196690, 196646, 196661, 196621, 196108, 196688, 196692, 196673, 196641, 196661, 196686, 196627, 196678, 195083, 196501, 196668, 196681, 196643, 196684, 196683, 196682, 196665, 196452, 196658, 196679, 196626, 179952, 196677, 195249, 196669, 180244, 196610, 196439, 196321, 196424, 196425, 196657, 196620, 196653, 196652, 196650, 196613,
            196640, 196641, 196642, 196643, 196644, 196646, 196626, 196627, 196638,
            196621, 196548, 196561, 193777, 185811, 195080, 195081, 196630, 196624,
            196623, 196631, 196633, 196634, 196564, 196635, 196588, 196427, 196637,
            196639, 196625, 196628, 196629, 196610, 196150, 174335, 196612, 196618,
            196611, 187993, 196572, 196434, 196501, 196382, 179857, 195082, 196223):
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)
    thread_summary(tid, near='999999')

# === ПРАВИЛО «БЫСТРЫЙ ТРЕД — ТРИ СЛЕПКА» (урок 54-92 interim: дыра #22-41 у 196707) ===
# При приросте LPN >15 постов/час добираем середину near=(prevLPN+LPN)//2,
# иначе хвост (20 постов на страницу) + прошлый слепок оставят дыру в середине.
PREV_LPN = {195081: 1076, 196718: 115, 196721: 18, 196727: 38, 196730: 32, 196732: 27, 196734: 53, 196735: 38, 196739: 13, 196742: 13, 196745: 14, 196747: 4, 196748: 32, 196749: 18, 196750: 13, 196752: 19, 196754: 11, 196757: 1, 196760: 32, 196756: 23, 196763: 32, 196762: 2, 196755: 33, 196758: 21, 196764: 7, 196765: 8, 196761: 18, 196766: 1, 196767: 5, 196768: 6, 196770: 65, 196771: 10}  # 54-122: 196770 ЗАТУХ 64->65 (+1/час, пик пройден, штаб EXENS не ответил); 196755 3-Й ЧАС 24->33 (+9, две волны); 196771 флейм +2 ->10; 196702 ожил +1 (41); 187993 Братство +6 (LPN 1207); 191614 Кот-арбуз +1 (7042); 112917 вайб вернулся (66429); затишье 196761/196765/196735/196756
print('\n===== FAST-RULE: середина для быстрорастущих (>15/час) =====')
for _tid, _plpn in PREV_LPN.items():
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
            print(f'[fast-rule] {_tid}: LPN {_plpn}->{_lpn} (delta {_delta}) <=15 — middle не нужен')
    except Exception as _e:
        print(f'[fast-rule] {_tid} fail: {_e}')

print('\n===== БОЛЬШИЕ ТРЕДЫ (cc из front-атрибутов) =====')
for i in front:
    if str(i.get('id')) in ('112917', '164665', '167367', '186525', '187993'):
        a = i.get('attributes', {})
        print(f"  [{i.get('id')}] cc={a.get('commentCount')} last={a.get('lastPostedAt','?')[:16]} :: {a.get('title','')[:60]}")

print(f'\nTS={TS}')
