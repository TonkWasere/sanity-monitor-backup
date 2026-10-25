#!/usr/bin/env python3
# gen54_224.py — цепная генерация rescan54_224_fetch.py из rescan54_223_fetch.py
# Строгие REPL: каждый old должен встретиться ровно 1 раз, иначе fail.
import py_compile, sys

SRC = '/home/z/my-project/tools/rescan54_223_fetch.py'
DST = '/home/z/my-project/tools/rescan54_224_fetch.py'
src = open(SRC, encoding='utf-8').read()

repls = [
# R1: шапка
("""# rescan54_223_fetch.py — Task 54-223: штатный часовой cron-раунд
# ~14:20 UTC 25.10, окно 13:20->14:20, база дельт — prev_lpn_224 (13:20,
# 54-222, state_snapshots git-tracked, 168 ключей).
# WIPE-40 (6-й откат ВМ за сутки, счёт 40/24ч — ВМ болеет смертно):
# recovery АВТОНОМЕН (12-й прогон, 13:55-14:00 UTC, начал lite s15):
# fetch+reset 71c70b8->0fa8442e + restore_state (prev_lpn_224 168 кл ->
# /tmp) + MEGA-vault (sha256 7f9edd5d = эталон, MAC OK, API 200, НЕ
# ротирован) + creds user:pass + helper store; bundle НЕ успел —
# создаёт 54-223 (шаг 4).
# Lite 13:40: GRADUATED 196997 «рейджбайт» 19/19. Lite 13:55: 196999
# 18/18 (+2), 196998 19/17 стоит. Lite 14:10: GRADUATED 196998/196999 —
# YOUNG-ВОЛНА УТРА ЗАКРЫТА (7 тредов 196993-196999, все graduated).
# Watch: ★ 196998 ОТС финал (19/17 — ГЭП 2 = 2 вырезанных поста);
# ★ 196999 лоты финал (18/18); ★ 196972 «Баланс STALZONE» (+9 в 54-222,
# 53/52 — новый горячий); ★ 196973 «Тред худшего игрока» (+8, 42/42);
# ★ 196943 фармер-волна (255/253 — к 300?); ★ stm-волна 196989 (41/40),
# 196987 (27/27), 196986 (32/32); ★ 196949 пауза 9-й час? (60/60);
# 196948 ВЫРЕЗ #41 (44/43); 196974 арена (41/41); 196982 (30/30);
# канон 97-й?; Санити 97-й; GG 73-й; ОТС 190; флешмоб 152-й; 404 132-й;
# ТГК #3240? (тишина с 3239 11:45Z); PAT №86 (ротации нет)""",
"""# rescan54_224_fetch.py — Task 54-224: штатный часовой cron-раунд
# ~15:20 UTC 25.10, окно 14:20->15:20, база дельт — prev_lpn_225 (14:20,
# 54-223, state_snapshots git-tracked, 169 ключей).
# WIPE-41 (7-й откат ВМ за сутки, снова к 71c70b8 19.10, счёт 41/24ч —
# ВМ болеет смертно): recovery АВТОНОМЕН (13-й прогон, 15:22-15:30 UTC,
# начал lite s15 15:10): clone+rsync (creds УЖЕ пропали с ВМ — clone
# публичный) + fetch+reset 71c70b8->356b0dd5 + restore_state (prev_lpn_225
# 169 кл -> /tmp) + helper store; PAT_VAULT_LOCAL.md и MEGA-vault-инстр
# потеряны с откатом → PUSH PENDING, нужен PAT №87 от автора.
# Lite 14:40: 197003 9/9->16/15 (+7, ВЫРЕЗ+1 гэп 0->1), 197004 +2.
# Lite 14:55: NEW 197005 «отс» 2/2, 197003 +5 (21/20), 197002 +3 (7/7),
# 197004 +1. Lite 15:10: SKIPPED (WIPE-41 — скрипт пропал).
# Watch: ★ 197003 «А собственно где?» (21/20, гэп 1 — ВЫРЕЗЫ пошли?);
# ★ 197004 «Предложение по цепи распада» (4/4); ★ 197005 «отс» (2/2,
# второй ОТС-тред дня после 196998); 197002 (7/7); ★ 196998 ОТС гэп 2->
# 3?; 196999 лоты гэп 1; ★ 196972 «Баланс STALZONE» (55/54 — рост
# продолжился в 14:20 снапе); ★ 196973 «Тред худшего» (44/44); ★
# 196943 фармер-волна (256/254 — к 300?); ★ 196949 пауза 10-й час?
# (60/60); 196948 ВЫРЕЗ #41; канон 98-й?; Санити 98-й; GG 74-й; ОТС
# 191; флешмоб 153-й; 404 133-й; ТГК #3240? (тишина с 3239 11:45Z);
# PAT №87 (creds потеряны WIPE-41 — ротация)"""),
# R2: TS
("TS = '20261025_1420'", "TS = '20261025_1520'"),
# R3: окно
("WIN = '2026-10-25T13:20'  # окно 13:20->14:20 (штатный час; WIPE-40 recovery автономный 13:55-14:00; lite: GRADUATED 196997/196998/196999 — young-волна закрыта)",
 "WIN = '2026-10-25T14:20'  # окно 14:20->15:20 (штатный час; WIPE-41 recovery автономный 15:22-15:30; lite: NEW 197005, 197003 разгон +12 с ВЫРЕЗом, 15:10 skipped)"),
# R4: загрузка базы дельт
("prev = json.load(open('/tmp/prev_lpn_224.json'))",
 "prev = json.load(open('/tmp/prev_lpn_225.json'))"),
# R4b: строка о базе
("print(f'(база prev_lpn_224: {len(prev)} ключей, 13:20 UTC — 54-222 штатный час)')",
 "print(f'(база prev_lpn_225: {len(prev)} ключей, 14:20 UTC — 54-223 штатный час)')"),
# R5: сохранение нового снапа
("json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_225.json', 'w'))",
 "json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_226.json', 'w'))"),
# R5b: строка о сохранении
("print(f'>>> prev_lpn_225.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')",
 "print(f'>>> prev_lpn_226.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')"),
# R6: заголовок секции дельт
("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_224 (база 13:20 — 54-222 штатный час, state_snapshots git-tracked) =====",
 "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_225 (база 14:20 — 54-223 штатный час, state_snapshots git-tracked) ====="),
# R7: WATCH — молодые 197003/704/705 в голову
("WATCH = [196999, 196998, 196972, 196973, 196997,",
 "WATCH = [196999, 196998, 197005, 197004, 197003, 196972, 196973, 196997,"),
# R8a: резюме — молодые после 196999
("print('\\n===== КЛЮЧЕВЫЕ РЕЗЮМЕ =====')\nthread_summary(196998)\nthread_summary(196999)\nthread_summary(196972)",
 "print('\\n===== КЛЮЧЕВЫЕ РЕЗЮМЕ =====')\nthread_summary(196998)\nthread_summary(196999)\nthread_summary(197005)\nthread_summary(197004)\nthread_summary(197003)\nthread_summary(196972)"),
# R8b: резюме — 196997 после 196973
("thread_summary(196972)\nthread_summary(196973)\nthread_summary(196997)",
 "thread_summary(196972)\nthread_summary(196973)\nthread_summary(196997)\nthread_summary(197002)"),
# R9: KNOWN — добавить 197002-197005
("196998, 196999, 196899, 131836, 196778}",
 "196998, 196999, 197002, 197003, 197004, 197005, 196899, 131836, 196778}"),
# R10: DONE-строка
("DONE 54-223 HOURLY PHASE1+2", "DONE 54-224 HOURLY PHASE1+2"),
]

for i, (old, new) in enumerate(repls, 1):
    n = src.count(old)
    if n != 1:
        print(f'FAIL R{i}: old встречается {n} раз (ожидался 1)'); sys.exit(1)
    src = src.replace(old, new)
    print(f'R{i} OK')

open(DST, 'w', encoding='utf-8').write(src)
py_compile.compile(DST, doraise=True)
print('py_compile OK ->', DST)
