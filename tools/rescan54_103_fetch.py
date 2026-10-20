# rescan54_103_fetch.py — Task 54-103: часовой cron-раунд ~07:30 UTC 20.10 (10:30 МСК 20.10).
# База = 54-102 (06:48 UTC, af9e402; обе репы = eebc3a9/af9e402, одиннадцатый подряд
# полный зелёный цикл). creds/vault/bundle на месте — ТОКЕН ПО-ПРЕЖНЕМУ НЕ РОТИРОВАН (5-е
# напоминание автору: живой ghp_ с 18.10 на публичной MEGA-ссылке, чистки не решают).
# Блок fast-rule в конце («БЫСТРЫЙ ТРЕД — ТРИ СЛЕПКА»): при delta LPN >15/час добирается
# середина; PREV_LPN={195081:1065, 196721:13, 196718:24}.
# СЛЕДИТЬ: ИТОГИ ОТС? (196424=160 тишина 38.5+ ч; 196425=124); ★ NEW 196727 «вопросик
# маленький» (Bulba2019) подрастёт?; ★ клан-жалоба 196689 21-й час? (114, LPN 117 —
# вспышка +8 в 54-102); mamich: 196718 замер (24)/196721 (13) — снос?; 196722 (6)/
# 196720 (4); NEW 196724 «Калибры» (6)/196725 «Плиты» (4); stm-выжившие 196706 (49
# флагман)/196704 (30 разгон)/196716 (27)/196702 (22)/196709 (20)/196708 (17)/196701
# (23)/196705 (22)/196715 (14)/196714 (13); КОНКУРС спал 195081 (1018, LPN 1065)/195080
# (779)/195083 (176); СНОСЫ 196411 16-й час? (#90?, LPN=89, гэпы [15,33,63-77,88]);
# @Marxont 24-й час? (196501=150); флешмоб талонов 25-й час? (196452 cc=30); ТГК 3217?
# (3216 последний 15:00, пауза 16.5 ч); 404-КОНТРОЛЬ: 196707 + 196717 (12-й час).
# База №145 (06:48 UTC, TS 0634+0640): ★ NEW 196727 «вопросик маленький» НАСТОЯЩИЙ
# (createdAt 06:28:16 — СОЗДАН ПРЯМО ВО ВРЕМЯ ОБХОДА, OP Bulba2019, cc=1: «сегодня
# с утра я зашел на дс сервер проекта АНОМА (не реклама), там в сливах группа
# разработчиков предлагает игрокам выбрать между 2 версиями инвентаря») — первая
# real-NEW с №143, счёт 54-69: 34/41 за 21 раунд; ★★ КЛАН-ЖАЛОБА 196689 20-Й ЧАС
# ВСПЫШКА +8 (cc 106→114, LPN 109→117, НОЛЬ удалений: все #110-117 видимы; флейм
# кланы+лудка: ave_tpecka «я инактив в кланах. Межсезон+заебала лудка», kukuha_edet
# «прост перестал ящики покупать», СерегаАвтосервис «я же не долбоеб, чтобы в кланах
# играть», Арига «ты просто не распробовал») — второй максимум серии после +10
# (№138); ★★ MAMICH-ПОТОК ЗАТИХ БЕЗ СНОСОВ: 196718 ЗАМЕР (24, delta 0 после 3 часов
# роста), 196721 +1 (12→13), 196722=6/196720=4 замер — ноль сносов 11-Й ЧАС ПОДРЯД;
# ★ STM-ПУЛ РАЗГОН: 196704 +6 (24→30, cc=LPN=30 всё видимо; флейм «заметность
# тайников»: The_Creatorr «если разрабы будут и дальше плодить синие рюкзачки»,
# Rodzya «АУ, В ВАШУ ИГРУ НЕ ТОЛЬКО ДЕТИ ИЗ 2Б ИГРАЮТ», Komrig «как в последней
# расомахе? Обоссать всё ЖЁЛТЫМ»), 196709 +3 (17→20, «Снова рейтинг» 06:20), 196702
# +2 (20→22), 196706 ФЛАГМАН +1 (48→49), 196708 +1 (16→17); замер: 196701=23 (LPN
# 24), 196705=22, 196716=27, 196715=14, 196714=13, 196703=7; NEW-треды замер: 196724
# «Калибры»=6, 196725 «Плиты»=4; ИТОГИ ОТС НЕ ВЫШЛИ (196424=160 тишина 38.5+ ч;
# 196425=124) — час 34 после закрытия; 196411 15-Й ЧАС БЕЗ СНОСОВ (LPN=89, cc=84,
# гэпы [15,33,63-77,88] неизменны, канон #48 off20+off40 CANON OK rx=0); 196699 слухи
# +2 (25→27, LPN 29); 196667 ппшки +1 (124, LPN 127); 196665=38/196624=58 замер;
# @Marxont 23-Й ЧАС (196501=150); флешмоб 24-Й ЧАС (196452=30, ~153 ч офиц. молчания);
# ТГК 3217 НЕТ (пауза 15.5 ч); Crios ~63 ч (196480=171); КОНКУРС спал (195081=1018
# LPN 1065 delta 0, 195080=779, 195083=176); фон замер: 196626=176, 196621=85,
# 196435=156, 196428=33, 196488=45, 196511 cc=31/LPN 39, 196524 Глеб 1147 LOCKED,
# 196475=252, 196532=333, 196496=103, 196260=59, 196078=74, 196062=54; контролы
# 196315=87/196415=6/196283=82 чисто; БОЛЬШИЕ: вайб 112917=66385 (06:08, +15, живой
# на фронте), rule34 164665 вне off0 (урок 54-88); fast-rule ×3 (delta 0/1/0).

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
         196658, 196661, 196656, 196665, 196667, 196668, 196666, 196321, 196439, 196669, 196670, 196673, 196677, 196679, 196647, 196678, 196681, 196682, 196683, 196684, 196685, 196686, 196651, 196688, 196689, 196660, 196690, 196691, 196692, 196697, 196698, 196699, 196700, 196701, 196703, 196704, 196702, 196706, 196707, 196708, 196709, 196705, 196714, 196715, 196716, 196717, 196718}

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
    if a.get('lastPostedAt','') >= '2026-10-20T06:27' or mark:
        print(f"  [{did}] {a.get('lastPostedAt','?')[:16]} cc={a.get('commentCount')} :: {a.get('title','')[:80]}{mark}")
print(f'>>> NEW front threads to OP-fetch (phase 2): {new_front}')

print('\n===== 196452 Талоны PvE (~154 ч офиц. молчания) =====')
thread_summary(196452)

print('\n===== 196511 Хотфикс (жетоны-пропажа; был cc=31, 3-и сутки) =====')
thread_summary(196511)

print('\n===== 196488 Кейс =====')
thread_summary(196488)
print('\n===== 196480 Кейс-шансы (был cc=171; Crios-тишина ~63 ч) =====')
thread_summary(196480)

print('\n===== 196524 Глеб (был cc=1147 LOCKED) =====')
thread_summary(196524)
print('\n===== 196475 Амнистия (был cc=252) =====')
thread_summary(196475)
print('\n===== 196522 Штыриуса тред =====')
thread_summary(196522)
print('\n===== 196523 ОБРАЩЕНИЕ К EXBO =====')
thread_summary(196523)

print('\n===== 196411 / #48 канон + union-карта (гэпы [15,33,63-77,88], волна 16-й час — следим #90+) =====')
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

print('\n===== 196532 Тирлист Завозов (был cc=292) =====')
thread_summary(196532)
print('\n===== 196536 Смена оружия (был cc=8) =====')
thread_summary(196536)
print('\n===== 196533 Американская гитара (был cc=2) =====')
thread_summary(196533)

print('\n===== 196537 Мастерский детектор прикопов (был cc=35) =====')
thread_summary(196537)
print('\n===== 196539 Вылеты vs Передовой кейс (был cc=30) =====')
thread_summary(196539)

print('\n===== 196424 ОТС (ЗАКРЫЛОСЬ 20:59 UTC, снят с закрепа 00:40, тишина 34.5+ ч, ИТОГИ = день 20.10, ждём; был cc=160) =====')
thread_summary(196424)
print('\n===== 196425 ОФИЦ. СБОР ФИДБЕКА ОТС (был cc=124; итоги ОТС = НЕ ВЫШЛИ 34.5+ ч) =====')
thread_summary(196425, near='999999')

print('\n===== 196461 Раздутый ттк =====')
thread_summary(196461)
print('\n===== 196435 Колизей-калибровка (был cc=154) =====')
thread_summary(196435)
print('\n===== 196510 КАЛЛибровка-2 (был cc=26) =====')
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

print('\n===== ТГК stalzone page0 (3217? пауза 16.5 ч после 3216@15:00) =====')
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

print('\n===== Хвосты окна 54-103: mamich-поток 196718/196721 + NEW 196727/196722/196724/196725 + stm-выжившие + 404-контроль =====')
for tid in (196727, 196725, 196724, 196722, 196721, 196720, 196718, 196655, 196705, 196714, 196715, 196716, 196717, 196702, 196706, 196709, 196707, 196708, 196701, 196704, 196703, 196692, 196688, 196699, 196700, 196698, 196689, 196667, 196697, 196686, 196548, 195080, 195081, 195083, 196690, 196646, 196661, 196621, 196108, 196688, 196692, 196673, 196641, 196661, 196686, 196627, 196678, 195083, 196501, 196668, 196681, 196643, 196684, 196683, 196682, 196665, 196452, 196658, 196679, 196626, 179952, 196677, 195249, 196669, 180244, 196610, 196439, 196321, 196424, 196425, 196657, 196620, 196653, 196652, 196650, 196613,
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
PREV_LPN = {195081: 1065, 196721: 13, 196718: 24}  # 54-102: 195081 LPN 1065 (cc=1018, спал delta 0); 196721 +1 -> 13; 196718 замер delta 0 -> 24
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
    if str(i.get('id')) in ('112917', '164665', '167367'):
        a = i.get('attributes', {})
        print(f"  [{i.get('id')}] cc={a.get('commentCount')} last={a.get('lastPostedAt','?')[:16]} :: {a.get('title','')[:60]}")

print(f'\nTS={TS}')
