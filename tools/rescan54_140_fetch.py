# rescan54_140_fetch.py — Task 54-140: часовой cron-раунд ~21:30 UTC 21.10 (00:30 МСК 22.10) —
# ШТАТНЫЙ. ПРИОРИТЕТ №1 = ПОСТ САНЕТИ 8-Й ЧАС + GETGOOD-ЯКОРЯ: база межраунда (54-139b, TS 2116) —
# cc/LPN 14454/14599 (+3 после вспышки ТГК: #14597 21:02 LordZoHbl «я не раб, а Властелин»,
# #14598 21:12 «те кто делают задания для ивентов знают?)», #14599 21:13 _VorT_ «Тёмненький»);
# GG-ЯКОРЯ база 21:02: #14590 rx{33:2} = ТОЧЕЧНАЯ реакция — АВТОРСКАЯ АТРИБУЦИЯ: «прирост это другой
# юзер заценил новейший пост» (НЕ прогулка GetGood, НЕ второй читатель); синхронный прирост = прогулка.
# ★★★ МЕЖРАУНД 54-139b (21:14-21:17): ОТКРОВЕНИЯ СПЕКТРУМА ПОДТВЕРЖДЕНЫ — ТГК-вспышка spectrum_zone
# 21:00-21:03 UTC после 6 ч тишины: 7929 карточки игроков Арены; 7939 ЛИГОВАЯ СИСТЕМА ПРАЗДНЕСТВА
# («Истерзанность»->«Прозрение» линейно, дальше двусторонний рейтинг, «Избавление» высшая — НЕ равно
# патчевым лигам 7843 МРАК/ЛУЧ/ПУЛЬСАР/КВАЗАР/СИНГУЛЯРНОСТЬ/ГОРИЗОНТ = ДВЕ системы за день);
# 7941 обзоры KreeNoLeeN + Мистер Жаби Жаби; 7942 реран Арены 28.10 (шмотка одним чертежом вместо 3,
# +5 за каждый; артефакты удвоением характеристик); ID-ГЭП 7895->7929 (33 ID) поверх дыры 7893/7894,
# лента отдала только 4 поста; «из Интересного» на форуме НЕТ (65 слагов проверено) — источник автора
# вне гостевого доступа. Форум-эхо синхронно ТГК-вспышке (159759 #14597 21:02).
# КОНТЕКСТ 54-139 (20:29-20:41): РЕСТ ПОСТА ПРЕРВАН +5 (#14592-96 20:02-20:25, баганые клан-паки:
# LordZoHbl ×3, stm:…57085, _VorT_; Crios НЕ ответил; грубый пинг Crios'у #14592 — 2-й за вечер);
# 196810 +10 (51) 8-Й ЧАС абус-тред: офиц. ответа нет, Kolbasavyalaya ×3, мод-реакции на #35 нет;
# NEW 196812 = ЛОЖНЫЙ (createdAt 17:35 < катофф, урок 54-136 повтор); остыли 196799 (67, 5-й час),
# 196809 (31, фармер СТОП), 196805 (31), 196791 (58, 11-й час); вырез-линия ЧИСТА (65 ключей).
# УРОКИ 54-113..139b: обход делить сразу (foreground timeout 585с + sed-finisher с фикс. TS и родным
# SKIP); фоновые запуски среда убивает молча; шапка заменяется ЦЕЛИКОМ по якорю начала строки
# «\\nimport json» (в шапках-уроках сам текст встречается — брать только начало строки; 24 раунда);
# 1-3 добора до EXIT=0; два TS-слоя — НОРМА; PREV_LPN по ВСЕМ замерам ledger прошлого раунда + поправка
# межраунда (54-140: 159759:14599); при взрыве NEW-треда — OP near=1 в фазе-2 (БЕЗ include — HTTP 400,
# урок 54-131); NEW-окно по lastPostedAt пропускает треды, созданные до катоффа (урок 54-136) —
# перепроверка createdAt ВСЕГДА; модерация может стереть тред целиком (196796, урок 54-136b) —
# снапы обязательны каждый раунд; авторство поста = relationships.user.data.id (урок 54-137);
# NEW фаза-2 = near1 + near999999 ОБА (54-138); TG-верификация по сырому HTML data-post= (54-138);
# канон-чек #48 = ВНУТРЕННЯЯ sha256 канон-поста из off20/off40 (54-139); GG без синхронности =
# точечная реакция (54-139, автор подтвердил 54-139b); ГОЛЫЙ near= гость ИГНОРИРУЕТ (отдаёт начало
# треда студами) — правильный параметр page%5Bnear%5D=N, URL-encode скобок (урок 54-139b);
# near999999 = последняя СТРАНИЦА (~20 постов) — якоря добирать near=<номер> (54-135b).
# СЛЕДИТЬ (54-140): 159759 ПЕРВЫЙ (8-й час: флейм баг-паков продолжится? Crios? мод-реакция? офиц.
# ответ?); GETGOOD-ЯКОРЯ (база 21:02): точечные дельты = шум читателей, СИНХРОННЫЙ прирост = прогулка;
# ТГК 7943+ (хвост откровений Спектрума: награды/шкала продолжение? сверка лиг vs 7843); 196810
# (офиц. ответ по абусу? мод-реакция на #35? от 51); 196817 (Культисты, вспух 2-й час — от 24);
# 196813/196816 (арт-залив от 19/16); 196812 (фарм-тред от 10); 196805/196809 (схрон/фармер —
# реанимация? от 31/31); 196799 (погас окончательно? от 67); 196791 (12-Й ЧАС? от 58); 196796
# ВЕРНУЛСЯ? (контроль возврата 5-Й ЧАС 404); 196411 сносы 14-Й ЧАС? (канон #48); 191614 (фон 7228);
# ТГК 3224/7943+ (гэпы 7893/7894 + 7896-7928); Арена 28.10; #SZFRAGMENTS 28.10; ИТОГИ ОТС час 72;
# флешмоб талонов 62-Й ЧАС (~191 ч); 196511 6-е сутки; Crios ~102 Ч (196480/196488); клан-жалоба
# 31-Й ЧАС; 404-контроли 49-Й ЧАС.
# База №181 + №181-Б (TS 2031 + межраунд 2116, 20:29-21:17 UTC): run1 EXIT=0 ДВЕНАДЦАТЫЙ раунд подряд;
# fast-rule ×0; NEW 196812 = ложный; вырез-линия чиста; Пост Санити 7-й час: рест прерван +5, GG-дельта
# #14590 = другой юзер (автор); межраунд: откровения Спектрума 7929/7939/7941/7942, 159759 +3 эхо;
# git 17ea38f (54-139b) = обеим репам, bundle 2118.

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
get('https://t.me/s/spectrum_zone', f'tg_spectrum_page0_{TS}.html', validate_json=False); time.sleep(1)
get(f'{BASE}/api/discussions?filter[q]=%D0%BB%D0%B5%D0%B3%D0%B5%D0%BD%D0%B4%D0%B0&page[offset]=0', f'search_legenda_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/194758?page[near]=999999', f'discussion_194758_near999999_{TS}.json'); time.sleep(1)

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
# GETGOOD-якоря (54-135b): старые посты автора НЕ попадают в near999999 (последняя страница) —
# добор near=<номер>: #69 (195574), #387 (195660), #48 (196411)
get(f'{BASE}/api/discussions/195574?page[near]=69', f'discussion_195574_near69_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/195660?page[near]=381', f'discussion_195660_near381_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196411?page[near]=48', f'discussion_196411_near48_{TS}.json'); time.sleep(1)
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
         196658, 196661, 196656, 196665, 196667, 196668, 196666, 196321, 196439, 196669, 196670, 196673, 196677, 196679, 196647, 196678, 196681, 196682, 196683, 196684, 196685, 196686, 196651, 196688, 196689, 196660, 196690, 196691, 196692, 196697, 196698, 196699, 196700, 196701, 196703, 196704, 196702, 196706, 196707, 196708, 196709, 196705, 196714, 196715, 196716, 196717, 196718, 196727, 196730, 196731, 196732, 196733, 196734, 196735, 196736, 196737, 196724, 196739, 196742, 196745, 196747, 196750, 196748, 196749, 196719, 196752, 196754, 196757, 196760, 196756, 196729, 196763, 196762, 196755, 196758, 196764, 196765, 196761, 196766, 196767, 196768, 196770, 196771, 196777, 196773, 196772, 196782, 196781, 196778, 196784, 196785, 196783, 196786, 196787, 196791, 196794, 196788, 196369, 174560, 196795, 196797, 196796, 196801, 196799, 196803, 196804, 196805, 196808, 196809, 196810, 196811, 196813, 196815, 196816, 196817, 196812}

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
    if a.get('lastPostedAt','') >= '2026-10-21T20:31' or mark:
        print(f"  [{did}] {a.get('lastPostedAt','?')[:16]} cc={a.get('commentCount')} :: {a.get('title','')[:80]}{mark}")
print(f'>>> NEW front threads to OP-fetch (phase 2): {new_front}')

print('\n===== SEARCH «легенда» (волна клуб-запросов 194758-типа?) =====')
try:
    _sl = json.load(open(os.path.join(OUT, f'search_legenda_{TS}.json')))
    for _i in (_sl.get('data') or [])[:10]:
        _ia = _i.get('attributes', {})
        print(f"  [{_i.get('id')}] cc={_ia.get('commentCount')} last={_ia.get('lastPostedAt','?')[:16]} :: {_ia.get('title','')[:80]}")
except Exception as _e:
    print(f'search parse fail: {_e}')

print('\n===== 194758 «Новый раздел для легенд» (cc=71; Pledik/Raonix ноют про клуб — движение?) =====')
thread_summary(194758)

print('\n===== 196452 Талоны PvE (~191 ч офиц. молчания, флешмоб 62-Й ЧАС?) =====')
thread_summary(196452)

print('\n===== 196511 Хотфикс (жетоны-пропажа; был cc=31, 6-е сутки (УТОЧНЕНО: createdAt 15.10 19:34 UTC); ПАТЧ ВЫШЕЛ — чейнджлога нет нигде, 196511 молчит) =====')
thread_summary(196511)

print('\n===== 196488 Кейс =====')
thread_summary(196488)
print('\n===== 196480 Кейс-шансы (был cc=171; Crios-тишина ~102 ч) =====')
thread_summary(196480)

print('\n===== 196524 Глеб (был cc=1147 LOCKED) =====')
thread_summary(196524)
print('\n===== 196475 Амнистия (был cc=252) =====')
thread_summary(196475)
print('\n===== 196522 Штыриуса тред =====')
thread_summary(196522)
print('\n===== 196523 ОБРАЩЕНИЕ К EXBO =====')
thread_summary(196523)

print('\n===== 196411 / #48 канон + union-карта (гэпы [15,33,63-78,88]; сносов нет 14-Й ЧАС?; ПОСЛЕ ПАТЧА следим #92+/зачистки) =====')
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

print('\n===== 196532 Тирлист Завозов (был cc=343/LPN 344; стоит 359 после +14 в 54-133) =====')
thread_summary(196532)
print('\n===== 196536 Смена оружия (был cc=8) =====')
thread_summary(196536)
print('\n===== 196533 Американская гитара (был cc=2) =====')
thread_summary(196533)

print('\n===== 196537 Мастерский детектор прикопов (был cc=35) =====')
thread_summary(196537)
print('\n===== 196539 Вылеты vs Передовой кейс (был cc=30) =====')
thread_summary(196539)

print('\n===== 196424 ОТС (ЗАКРЫЛОСЬ 20:59 UTC, снят с закрепа 00:40, тишина 71.5+ ч, ЧАС 72, ИТОГИ так и не вышли ПОСЛЕ ПАТЧА; был cc=160) =====')
thread_summary(196424)
print('\n===== 196425 ОФИЦ. СБОР ФИДБЕКА ОТС (был cc=124; итоги ОТС = НЕ ВЫШЛИ 71.5+ ч, ЧАС 72) =====')
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

print('\n===== ТГК stalzone page0 (3224/3225?; последний 3223 фото 15:00 — 6.5+ ч тишины) =====')
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

print('\n===== ТГК Спектрума spectrum_zone page0 (7896/7897?; последний 7895 фото 15:03; 7893/7894 ДЫРА ID (удалены/зарезервированы); 7891 Арена 28.10) =====')
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

print('\n===== Хвосты окна 54-140: ПОСТ САНЕТИ 8-Й ЧАС — 159759 ПЕРВЫЙ (14454/14599: эхо ТГК-вспышки Спектрума #14597-99; флейм баг-паков продолжится? Crios? мод-реакция? офиц. ответ?) + 196812 10 лвл фейсита (10, ложный NEW — фарм-тред) + 196817 Культисты в Зоне (24, вспух 2-й час — kravv285 7-й тред) + 196813 Мой первый арт (19, арт-залив OP продолжится?) + 196815 проблема диска (7, помощь прилетит?) + 196816 Кот на голубом шаре (16) + 196810 Разраб красава (51, 8-Й ЧАС народный абус-тред — офиц. ответ? мод-реакция на #35?) + 196809 Я не могу выбрать (31, фармер СТОП) + 196811 ПАХАН БОРЬБА (5, мод-пинг Terraman без ответа) + 196805 Диггерские байки (31, схрон найдут?) + 196808 Долбаные текстуры (6) + 196803 Краш после загрузки мира (20) + 196804 OlderZ (4) + 196796 По-русски говори (КОНТРОЛЬ ВОЗВРАТА 5-Й ЧАС — снесён подтв. автором) + 196801 Как стакать запчасти (13) + 196799 Тихо шифером шурша (67, погас окончательно?) + 196795 Зона в кадре (11, #SZFRAGMENTS старт 28.10) + 196797 Штурму даром (35) + 196794 Гжель (25) + 196791 (58, 12-Й ЧАС?) + 196788 (45) + 196778 (41, офиц. ответ 9+ ч?) + 196784 Воздухан (40) + 196785 Лаунчер (26) + 196783 (13)/196772 (33)/196782 (7 LOCKED)/196781 (4) + 196777 (66) + 196773 ГЛЕБ-ЛОР (95) + 196771 (16) + 196770 (124, Crios vs AlexMrz2) + 196767 (34)/196763 (50)/196761 (30) + 196757 техработы (1) + прямые замеры 191614 (7228, фон)/112917 (67705) + 196749 споты (44) + mamich-поток 196718 (115)/196721 (18) + 196755 (47)/196758 (25)/196760 (33) + вчерашние NEW 196756 (23)/196754 (11)/196752 (28)/196750 (13)/196748 (45)/196747 (4)/196745 (14)/196739 (13)/196742 (13)/196737/196734 (55)/196735 (38)/196736/196732 (27)/196733/196730 (32)/196731/196727 (38) + stm-выжившие + 404-контроль (196707/196717 49-Й ЧАС; 196796 = возврат?) =====')
for tid in (159759, 196803, 196804, 196805, 196808, 196809, 196810, 196811, 196812, 196813, 196815, 196816, 196817, 196796, 196801, 196799, 196795, 196797, 196791, 196794, 196788, 196778, 196784, 196785, 196783, 196786, 196787, 196772, 196782, 196781, 196777, 196773, 196771, 196770, 196768, 196767, 196766, 196757, 196764, 196765, 196761, 196763, 196762, 196755, 196758, 196760, 196756, 196754, 196752, 196750, 196749, 196748, 196747, 196745, 196739, 196742, 196737, 196734, 196735, 196736, 196732, 196733, 196730, 196731, 196727, 196725, 196724, 196722, 196721, 196720, 196718, 196655, 196705, 196714, 196715, 196716, 196717, 196702, 196706, 196709, 196707, 196708, 196701, 196704, 196703, 196692, 196688, 196699, 196700, 196698, 196689, 196667, 196697, 196686, 196548, 195080, 195081, 195083, 196690, 196646, 196661, 196621, 196108, 196688, 196692, 196673, 196641, 196661, 196686, 196627, 196678, 195083, 196501, 196668, 196681, 196643, 196684, 196683, 196682, 196665, 196452, 196658, 196679, 196626, 179952, 196677, 195249, 196669, 180244, 196610, 196439, 196321, 196424, 196425, 196657, 196620, 196653, 196652, 196650, 196613,
            196640, 196641, 196642, 196643, 196644, 196646, 196626, 196627, 196638,
            196621, 196548, 196561, 193777, 185811, 195080, 195081, 196630, 196624,
            196623, 196631, 196633, 196634, 196564, 196635, 196588, 196427, 196637,
            196639, 196625, 196628, 196629, 196610, 196150, 174335, 196612, 196618,
            196611, 187993, 196572, 196434, 196501, 196382, 179857, 195082, 196223, 191614, 112917):
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)
    thread_summary(tid, near='999999')


print('\n===== GETGOOD-ДЕЛЬТА (54-135b: реакции на Санити-постах = u/GetGood, прогулялся по всем постам автора; маркер прогулки = синхронный прирост likes на якорях; база 21:02 UTC (54-139b межраунд: #14590 rx{33:2} — ТОЧЕЧНАЯ дельта, автор: «другой юзер заценил новейший пост», НЕ прогулка): #69 likes=1 rx{34:6}, #387 likes=1 rx{35:1}, #48 likes=2, #14590 likes=1 rx{33:2}, #14591 likes=1 rx{33:1}) =====')
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
anchor_like(159759, 999999, 14590, 1, {'33': 1})
anchor_like(159759, 999999, 14591, 1, {'33': 1})

print('\n===== RANKS (OP -> Flarum-группы; ГЕЙТ КУЗНИ ПОДТВЕРЖДЁН автором: sanity НЕ может создать тред, Болота открыты; порог <= Мастер) =====')
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
        print(f"[rank {tid}] OP={a.get('username')} groups={[groups.get(g, g) for g in gids]} join={(a.get('joinTime') or '?')[:10]} cc={a.get('commentCount')}")
    except Exception as e:
        print(f'[rank {tid}] fail: {e}')
for _rt in (196812, 196817, 196813, 196815, 196816, 196805, 196808, 196809, 196810, 196811, 196803, 196804, 196801, 196799, 196795, 196797, 196794, 196791, 196788, 196778, 196785, 196783, 196786, 196787):
    op_rank(_rt)

# === ПРАВИЛО «БЫСТРЫЙ ТРЕД — ТРИ СЛЕПКА» (урок 54-92 interim: дыра #22-41 у 196707) ===
# При приросте LPN >15 постов/час добираем середину near=(prevLPN+LPN)//2,
# иначе хвост (20 постов на страницу) + прошлый слепок оставят дыру в середине.
PREV_LPN = {191614: 7228, 196749: 44, 196755: 47, 196758: 25, 196770: 124, 196773: 95, 196777: 66, 196778: 41, 196794: 25, 196801: 13, 196803: 20, 196804: 4, 196805: 31, 196808: 6, 196809: 31, 196810: 51, 196811: 5, 196812: 10, 196813: 19, 196815: 7, 196816: 16, 196817: 24, 159759: 14599, 112917: 67705, 187993: 1251, 195081: 1076, 196718: 115, 196721: 18, 196727: 38, 196730: 32, 196732: 27, 196734: 55, 196735: 38, 196739: 13, 196742: 13, 196745: 14, 196747: 4, 196748: 45, 196750: 13, 196752: 28, 196754: 11, 196756: 23, 196757: 1, 196760: 33, 196761: 30, 196762: 4, 196763: 50, 196764: 11, 196765: 19, 196766: 1, 196767: 34, 196768: 8, 196771: 16, 196772: 33, 196781: 4, 196782: 7, 196783: 13, 196784: 40, 196785: 26, 196786: 36, 196787: 3, 196788: 45, 196791: 58, 196795: 11, 196797: 35, 196799: 67}  # 54-139 (№181) + межраунд 54-139b (159759:14599): ПОСТ САНЕТИ 7-Й ЧАС — РЕСТ ПРЕРВАН +5 (#14592-96 баганые клан-паки, LordZoHbl ×3), cc/LPN 14451/14596 -> 14454/14599 эхо ТГК-вспышки Спектрума (#14597-99 21:02-21:13); ОТКРОВЕНИЯ ПОДТВЕРЖДЕНЫ (7929/7939/7941/7942 @ 21:00-21:03: карточки Арены, лиги Празднества Истерзанность-Прозрение-Избавление, реран 28.10 — чертёж один вместо 3, артефакты ×2), ID-гэп 7895->7929; GG #14590 rx{33:2} = другой юзер (авторская атрибуция, НЕ прогулка); 196810 +10 (51, офиц. ответа нет), NEW 196812 ложный (10), остыли 196799 (67)/196809 (31)/196805 (31)/196791 (58); вырез-линия чиста; 196796 404 4-й час (возврата нет); 196411 сносов нет 13-Й ЧАС
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
