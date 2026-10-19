#!/usr/bin/env python3
# rescan54_91_fetch.py — Task 54-91: часовой cron-раунд ~19:30 UTC 19.10 (22:30 МСК).
# База = 54-90 (18:45 UTC, bc8f35a локально; remote 6dd7f4d — push pending 1 коммит).
# ⚠ PUSH PENDING 2-й раунд: creds-файл мёртв после отката ВМ (fetch жив — репа
# читается публично), АВТОРУ: новый PAT; ротация токена с 14:29 UTC 18.10 не
# сделана (публичная MEGA-ссылка). Локальная очередь: bc8f35a (54-90).
# Час 23 после закрытия ОТС — линия молчит; итоги/анонсы «Послезавтра»=20.10.
# СЛЕДИТЬ: 196707 «Бей своих» догорит или staff? (+30/час, 52 — флейм
# фурри/наёМыши/Завет); stm-пул 196706 «Юг/Север» (23) / 196708 (9) / 196709
# (8); клан-жалоба 196689 9-й час? (64 — рекорд серии); 195081 залив заявок?
# (984, LPN 1031); ппшки пауза после 7 ч (196667 116); СНОСЫ 196411 3-й час
# (#90?); ФЛЕШМОБ ТАЛОНОВ ПАУЗА 13-й час (196452 cc=30); ответ @Marxont
# (196501=149, 11 ч нет); итоги ОТС 20.10; ТГК 3217?
# healthcheck 19:27 = drift push-pending (bc8f35a vs 6dd7f4d — очередь 1),
# creds DEAD, bundle пересоздадим. Урок 54-90: снапшот ВМ откатывает диск —
# remote = истина, сверять worklog с git-историей.
# База №133 (18:45 UTC, TS 1833+1840): NEW ×1 НАСТОЯЩИЙ: 196702 «Новое
# целеполагание» (createdAt 16:07:16, OP Sgt_Fill, cc=4 — тред-невидимка:
# создан 16:07, ожил в окне 18:04-18:38); ВЗРЫВ ЧАСА: 196707 stm-тред +30
# (22→52, live 18:33 — флейм фурри/наёМыши/Завет, mamich2077kolhoz vs
# AleeoZAVET); STM-ПУЛ ЖИВ: 196706 +9 (23), 196708 +5 (9), 196709 +4 (8);
# stm-новые 54-88 замерли 2-й час (196701=15/196704=7/196703=4); КЛАН-ЖАЛОБА
# 196689 8-Й ЧАС — РЕКОРД СЕРИИ (+5, 64, LPN 65); ппшки 196667 ВСТАЛИ
# (первый ноль за 7 ч, 116, LPN 119); КОНКУРС-ВОЛНА: 195081 залив +7 (984,
# LPN 1031), 195080 +2 (751 — 4-й file:///C:/ за 2 дня), 195082 +1 (94),
# 195079 +1 (217); ожили: 196683 +7 (31), 196572 +1 (61), 196548 +3 (93);
# замерли: 196692 (22), 196688 (50), 196699 (18), 196700 (14), 196698 мёртв
# 3-й час (20), 196697 4-й час (10), 196646 (82), 196621 (85), 196108 (86),
# 196690 (25), 196661 (58), 196686 (39), 196681 (74), 195083 (175), KIM-X
# (121), 196641 (28), 196626 (176); СНОСЫ 196411 ТРЕТИЙ ЧАС БЕЗ СНОСОВ:
# гэпы [15,33,63-77,88], LPN=89, канон OK rx=0; офиц. линия час 22 (196424
# =160, 196425=124, 196480=171 Crios ~50 ч); ответа @Marxont нет 11-й час
# (196501=149); нули: 196684 (56 — ВОСЬМОЙ); ФЛЕШМОБ ТАЛОНОВ ПАУЗА 12-Й ЧАС
# (cc=30); ТГК 3216 (15:00) последний; 114800 «щитпостинг» cc=12698 вошёл в
# окно фронта (редкое); контролы 196315=87/196415=6/196283=82.
#
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
         185811, 196427, 196223, 195082, 196434, 196652, 196650, 196613, 196653, 196657,
         196658, 196661, 196656, 196665, 196667, 196668, 196666, 196321, 196439, 196669, 196670, 196673, 196677, 196679, 196647, 196678, 196681, 196682, 196683, 196684, 196685, 196686, 196651, 196688, 196689, 196660, 196690, 196691, 196692, 196697, 196698, 196699, 196700, 196701, 196703, 196704, 196702, 196706, 196707, 196708, 196709}

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
    if a.get('lastPostedAt','') >= '2026-10-19T18:33' or mark:
        print(f"  [{did}] {a.get('lastPostedAt','?')[:16]} cc={a.get('commentCount')} :: {a.get('title','')[:80]}{mark}")
print(f'>>> NEW front threads to OP-fetch (phase 2): {new_front}')

print('\n===== 196452 Талоны PvE (~144 ч офиц. молчания) =====')
thread_summary(196452)

print('\n===== 196511 Хотфикс (жетоны-пропажа; был cc=31, 3-и сутки) =====')
thread_summary(196511)

print('\n===== 196488 Кейс =====')
thread_summary(196488)
print('\n===== 196480 Кейс-шансы (был cc=171; Crios-тишина ~51 ч) =====')
thread_summary(196480)

print('\n===== 196524 Глеб (был cc=1147 LOCKED) =====')
thread_summary(196524)
print('\n===== 196475 Амнистия (был cc=252) =====')
thread_summary(196475)
print('\n===== 196522 Штыриуса тред =====')
thread_summary(196522)
print('\n===== 196523 ОБРАЩЕНИЕ К EXBO =====')
thread_summary(196523)

print('\n===== 196411 / #48 канон + union-карта (гэпы [15,33,63-77,88], волна встала 3-й час — следим #90+) =====')
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

print('\n===== 196424 ОТС (ЗАКРЫЛОСЬ 20:59 UTC, снят с закрепа 00:40, тишина 22.5+ ч, итоги ждутся 20.10; был cc=160) =====')
thread_summary(196424)
print('\n===== 196425 ОФИЦ. СБОР ФИДБЕКА ОТС (был cc=123 #129 20:07; «Послезавтра»=20.10) =====')
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

print('\n===== ТГК stalzone page0 (3217?) =====')
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

print('\n===== Хвосты окна 54-91: 196702 + stm-пул + сносы №133 =====')
for tid in (196702, 196706, 196709, 196707, 196708, 196701, 196704, 196703, 196692, 196688, 196699, 196700, 196698, 196689, 196667, 196697, 196686, 196548, 195080, 195081, 195083, 196690, 196646, 196661, 196621, 196108, 196688, 196692, 196673, 196641, 196661, 196686, 196627, 196678, 195083, 196501, 196668, 196681, 196643, 196684, 196683, 196682, 196665, 196452, 196658, 196679, 196626, 179952, 196677, 195249, 196669, 180244, 196610, 196439, 196321, 196424, 196425, 196657, 196620, 196653, 196652, 196650, 196613,
            196640, 196641, 196642, 196643, 196644, 196646, 196626, 196627, 196638,
            196621, 196548, 196561, 193777, 185811, 195080, 195081, 196630, 196624,
            196623, 196631, 196633, 196634, 196564, 196635, 196588, 196427, 196637,
            196639, 196625, 196628, 196629, 196610, 196150, 174335, 196612, 196618,
            196611, 187993, 196572, 196434, 196501, 196382, 179857, 195082, 196223):
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)
    thread_summary(tid, near='999999')

print('\n===== БОЛЬШИЕ ТРЕДЫ (cc из front-атрибутов) =====')
for i in front:
    if str(i.get('id')) in ('112917', '164665', '167367'):
        a = i.get('attributes', {})
        print(f"  [{i.get('id')}] cc={a.get('commentCount')} last={a.get('lastPostedAt','?')[:16]} :: {a.get('title','')[:60]}")

print(f'\nTS={TS}')
