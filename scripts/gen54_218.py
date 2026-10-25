#!/usr/bin/env python3
# gen54_218.py — цепная генерация rescan54_218_fetch.py из rescan54_217_fetch.py
# Строгие REPL: каждый old должен встретиться ровно 1 раз, иначе fail.
import py_compile, sys

SRC = '/home/z/my-project/tools/rescan54_217_fetch.py'
DST = '/home/z/my-project/tools/rescan54_218_fetch.py'
src = open(SRC, encoding='utf-8').read()

repls = [
# R1: шапка (база №257 -> №258, WIPE-35/36 recovery, watch-линия)
("""# rescan54_217_fetch.py — Task 54-217: штатный часовой cron-раунд
# ~08:20 UTC 25.10, окно 07:20->08:20, база дельт — prev_lpn_218 (07:20,
# 54-216, state_snapshots git-tracked).
# WIPE-34 (34-й откат ВМ, окно ~07:50-08:20, снова к 71c70b8 ~126 ч
# старья): пойманы s15 07:55/08:10 lite (tools отсутствовали → тихие
# скипы ×2; s35 07:35 и s15 07:40 успели до вайпа).
# Recovery АВТОНОМЕН ~2 мин (7-й прогон, рутинный): fetch+reset
# 71c70b8->826aa192 + creds из MEGA-vault (restore_creds_54_96, sha256
# 7f9edd5d = эталон, API 200, ls-remote OK) + helper store GLOBAL +
# vault перезаложен; prev_lpn_218 из state_snapshots -> /tmp.
# ПОТЕРИ: lite-строки worklog 07:35 (s35 NEW 196988) / 07:40 (s15
# RECONCILE ×2: 196989 5/5, 196990 4/4) не успели в коммит —
# восстановлены реплеем с пометкой.
# Watch: ★ 196988 «Читеры» (3/3, young); ★ 196989 stm «Накипело!» (5/5,
# young); ★ 196990 «Доставка П/Р/П» (4/4, young — резонанс?); ★ 196986
# stm-сборище (17/17, из young); 196987 (9/9); ★ 196974 арена — разгон
# продолжится? (27/27); ★ 196949 пауза 3-й час? (60/60); ★ 196948 ВЫРЕЗ
# #41 (44/43); 196984 (13/12); 196975 (28/28); 196943 гэп 2 (191/189);
# 196834 гэп 7 (66/59); канон 91-й; Санити 91-й; GG 67-й; ОТС 184;
# флешмоб 146-й; 404 126-й; ТГК 3238? (тишина 18-й час); PAT №80
# (ротации нет; 34 отката за сутки — ВМ мертвецки болен)""",
"""# rescan54_218_fetch.py — Task 54-218: штатный часовой cron-раунд
# ~09:20 UTC 25.10, окно 08:20->09:20, база дельт — prev_lpn_219 (08:20,
# 54-217, state_snapshots git-tracked, 159 ключей).
# WIPE-35+36 (два отката ВМ за ~80 мин: ~08:4x-08:55 и ~08:56-09:20,
# оба снова к 71c70b8 ~126 ч старья; счёт 36 за сутки): стёрты lite-
# скрипты (snap15/snapnew35), creds, vault, bundle; s15 08:55/09:10 и
# s35 09:35 — тихие скипы; s15 08:40 (196991 NEW + RECONCILE ×3)
# успел до вайпа — строка восстановлена реплеем.
# Recovery АВТОНОМЕН (8-й прогон): fetch+reset 71c70b8->086d3683 +
# creds из MEGA-vault (restore_creds_54_96, sha256 7f9edd5d = эталон,
# API 200, ls-remote OK) + helper store GLOBAL + vault перезаложен +
# /home/z/backups пересоздан; prev_lpn_219 из state_snapshots -> /tmp.
# Watch: ★ 196991 «А ведь интересно» (NEW young 08:40, 5/5, +4/5м);
# ★ 196988 «Читеры» (4/4, young, TTL ~09:40); ★ 196989 stm «Накипело!»
# (15/15, young); ★ 196990 «Доставка П/Р/П» (7/7, young); 196986 stm
# (17/17, из young); 196987 (9/9); ★ 196974 арена — 3-й час разгона?
# (38/38); ★ 196949 пауза 4-й час? (60/60); ★ 196948 ВЫРЕЗ #41 (44/43);
# 196984 (13/12); 196975 (28/28); 196943 гэп 2 (191/189); 196834 гэп 7
# (66/59); канон 92-й?; Санити 92-й; GG 68-й; ОТС 185; флешмоб 147-й;
# 404 127-й; ТГК 3238? (тишина 19-й час); PAT №82 (ротации нет;
# ВМ: 2 отката за час — болен смертно)"""),
# R2: TS
("TS = '20261025_0820'", "TS = '20261025_0920'"),
# R3: окно
("WIN = '2026-10-25T07:20'  # окно 07:20->08:20 (штатный час; ~07:50-08:20 WIPE-34, s15 07:55/08:10 скипнулись — покрыто этим обходом)",
 "WIN = '2026-10-25T08:20'  # окно 08:20->09:20 (штатный час; 08:4x-09:20 WIPE-35+36, lite-события 08:40 реплеем в worklog)"),
# R4: загрузка базы дельт
("prev = json.load(open('/tmp/prev_lpn_218.json'))",
 "prev = json.load(open('/tmp/prev_lpn_219.json'))"),
# R4b: строка о базе
("print(f'(база prev_lpn_218: {len(prev)} ключей, 07:20 UTC — 54-216 штатный час)')",
 "print(f'(база prev_lpn_219: {len(prev)} ключей, 08:20 UTC — 54-217 штатный час)')"),
# R5: сохранение нового снапа
("json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_219.json', 'w'))",
 "json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_220.json', 'w'))"),
# R5b: строка о сохранении
("print(f'>>> prev_lpn_219.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')",
 "print(f'>>> prev_lpn_220.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')"),
# R6: заголовок секции дельт
("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_218 (база 07:20 — 54-216 штатный час, state_snapshots git-tracked) =====",
 "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_219 (база 08:20 — 54-217 штатный час, state_snapshots git-tracked) ====="),
# R7: WATCH — 196991 в голову
("WATCH = [196988, 196989, 196990, 196986,", "WATCH = [196991, 196988, 196989, 196990, 196986,"),
# R7b: KNOWN — += 196991
("196985, 196986, 196987, 196988, 196989, 196990, 196899, 131836, 196778}",
 "196985, 196986, 196987, 196988, 196989, 196990, 196991, 196899, 131836, 196778}"),
# R8: ключевые резюме — 196991 в голову
("print('\\n===== КЛЮЧЕВЫЕ РЕЗЮМЕ =====')\nthread_summary(196988)",
 "print('\\n===== КЛЮЧЕВЫЕ РЕЗЮМЕ =====')\nthread_summary(196991)\nthread_summary(196988)"),
# R9: DONE-строка
("DONE 54-217 HOURLY PHASE1+2", "DONE 54-218 HOURLY PHASE1+2"),
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
