#!/usr/bin/env python3
# gen54_17.py — генерирует tools/rescan54_17_fetch.py из rescan54_16_fetch.py
# (цепочка 54-15→54-16→54-17; базлайны ledger №63, TS 1628/1631)
import io

SRC = '/home/z/my-project/tools/rescan54_16_fetch.py'
DST = '/home/z/my-project/tools/rescan54_17_fetch.py'

src = io.open(SRC, encoding='utf-8').read()

OLD_HEADER = """# rescan54_16_fetch.py — Task 54-16: часовой cron-раунд ~16:30 UTC 16.10 (19:30 МСК). Линии
# зелёные (dc39697). ПЕРВЫЙ ПОЛНЫЙ ЧАС ОТС (старт 15:00 UTC): наполнение офиц. фидбек-треда
# 196425 (был cc=4), доступ-жалобы 196424 (был cc=110), возобновятся ли сносы 196411 после
# паузы 2.75 ч (гэпов 12), компенсация: купленные Передовые (#83)/шансы/вторая волна,
# Глеб 728 / Тирлист 236 (гонка темпов), 196537 +19/ч, 196551/196539 молодые линии, ТГК 3206+."""

NEW_HEADER = """# rescan54_17_fetch.py — Task 54-17: часовой cron-раунд ~17:30 UTC 16.10 (20:30 МСК). Линии
# зелёные (18e8454). ЧАС+2 ОТС: реакция на ТГК 3206 (инвайт-письма пришли не всем?), наполнение
# 196425 (был cc=11), энергетик-волна компенсации 196557, сносы 196411 стоят 4.75+ ч (#73+?),
# темп 196552 «Новый движок» (был +43/ч), вылеты 196539 (был cc=21), Глеб 768 (4-й час пика),
# Тирлист 247, купленные Передовые (#83 без ответа 3.75 ч), ТГК 3207+."""

REPL = [
    (OLD_HEADER, NEW_HEADER),
    ("'2026-10-16T15:00'", "'2026-10-16T16:00'"),
    ('===== 196452 Талоны PvE (~49 ч офиц. молчания) =====', '===== 196452 Талоны PvE (~50 ч офиц. молчания) ====='),
    ('===== 196524 Глеб (был cc=728, +110/2ч) =====', '===== 196524 Глеб (был cc=768, +40/ч четвёртый час) ====='),
    ('===== 196532 Тирлист Завозов (был cc=236) =====', '===== 196532 Тирлист Завозов (был cc=247) ====='),
    ('===== 196539 Вылеты vs Передовой кейс (был cc=14) =====', '===== 196539 Вылеты vs Передовой кейс (был cc=21, +7/ч) ====='),
    ('===== 196424 ОТС (старт 15:00 UTC — час+1: фидбек/доступ) =====', '===== 196424 ОТС (старт 15:00 UTC — час+2: инвайты/фидбек) ====='),
    ('===== 196537 Мастерский детектор прикопов (был cc=28) =====', '===== 196537 Мастерский детектор прикопов (был cc=30) ====='),
    ('===== 196425 ОФИЦ. СБОР ФИДБЕКА ОТС (был cc=4/LPN8) =====', '===== 196425 ОФИЦ. СБОР ФИДБЕКА ОТС (был cc=11/LPN15) ====='),
    # KNOWN: + 196552/196557
    ("196425, 196551, 196541, 196542, 196543}",
     "196425, 196551, 196541, 196542, 196543, 196552, 196557}"),
    # phase-2 блок: хвосты 196552/196557/196537/196539 + младшие NEW (196541 выпал — мёртв cc=3)
    ("# --- хвосты: офиц. фидбек ОТС 196425 + 3д ДШД 196551 + вчерашие NEW 196541/196542/196543 ---\nget(f'{BASE}/api/discussions/196425?page[near]=999999', f'discussion_196425_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196551?page[near]=999999', f'discussion_196551_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196541?page[near]=999999', f'discussion_196541_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196542?page[near]=999999', f'discussion_196542_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196543?page[near]=999999', f'discussion_196543_near999999_{TS}.json'); time.sleep(1)",
     "# --- хвосты: 196425/196552/196557 + 196537/196539 + младшие NEW 196551/196542/196543 ---\nget(f'{BASE}/api/discussions/196425?page[near]=999999', f'discussion_196425_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196552?page[near]=999999', f'discussion_196552_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196557?page[near]=999999', f'discussion_196557_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196537?page[near]=999999', f'discussion_196537_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196539?page[near]=999999', f'discussion_196539_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196551?page[near]=999999', f'discussion_196551_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196542?page[near]=999999', f'discussion_196542_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196543?page[near]=999999', f'discussion_196543_near999999_{TS}.json'); time.sleep(1)"),
    # финальный блок NEW-тредов
    ("print('\\n===== NEW-треды окна 15:26: 196551/196541/196542/196543 (хвосты) =====')\nfor tid in (196551, 196541, 196542, 196543):\n    thread_summary(tid, near='999999')",
     "print('\\n===== NEW-треды окна 16:26: 196552/196557 + младшие (хвосты) =====')\nfor tid in (196552, 196557, 196551, 196542, 196543):\n    thread_summary(tid, near='999999')"),
]

for old, new in REPL:
    if old not in src:
        raise SystemExit(f'PATTERN NOT FOUND: {old[:80]!r}')
    src = src.replace(old, new, 1)

io.open(DST, 'w', encoding='utf-8').write(src)
print('written', DST, len(src), 'chars')
