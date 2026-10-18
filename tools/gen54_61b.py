#!/usr/bin/env python3
# gen54_61b.py — цепной генератор: rescan54_60b_phase2.py -> rescan54_61b_phase2.py
# NEW 54-61: 196653 «Завершение ОТС» (news, 14:27, cc=4), 196657 «Красный атом» (14:40, cc=3)
import sys, py_compile

SRC = '/home/z/my-project/tools/rescan54_60b_phase2.py'
DST = '/home/z/my-project/tools/rescan54_61b_phase2.py'

REPL = [
    ('''# rescan54_60b_phase2.py — Task 54-60 phase 2: OP (near=1) для NEW:
# 196652 «Загадочный тайник на Агрокомлексе» (cc=4, 13:35), 196650 «Мёртвый чат»
# (cc=12, 13:34), 196613 «Опрос на ОТС» (news-NEW, 17.10 16:58 — окно потери 54-37..54-59)''',
     '''# rescan54_61b_phase2.py — Task 54-61 phase 2: OP (near=1) для NEW:
# 196653 «Завершение ОТС» (news-NEW, 14:27, cc=4 — Официальное окончание теста 16-18.10),
# 196657 «Красный атом» (14:40, cc=3)'''),

    ('''for tid in (196652, 196650, 196613):''',
     '''for tid in (196653, 196657):'''),
]

out = open(SRC, encoding='utf-8').read()
for i, (old, new) in enumerate(REPL, 1):
    if old not in out:
        sys.exit(f'PATTERN NOT FOUND ({i}/{len(REPL)}): {old[:90]!r}')
    out = out.replace(old, new, 1)
open(DST, 'w', encoding='utf-8').write(out)
py_compile.compile(DST, doraise=True)
print(f'OK {DST} — {len(REPL)}/{len(REPL)} REPL, py_compile OK')
