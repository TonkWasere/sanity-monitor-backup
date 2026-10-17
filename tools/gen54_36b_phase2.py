#!/usr/bin/env python3
# gen54_36b_phase2.py — цепной генератор: rescan54_35b_phase2.py -> rescan54_36b_phase2.py
# Phase 2 раунда 54-36: OP NEW 196470 («Нервный срыв на колизее», cc=26) / 196606
# («Эта игра издевается надо мной») + хвосты движущихся по фронту 196469 (LR-300) / 196530 (Фпс Колизея).
import sys, py_compile

SRC = '/home/z/my-project/tools/rescan54_35b_phase2.py'
DST = '/home/z/my-project/tools/rescan54_36b_phase2.py'

REPL = [
    ('''# rescan54_35b_phase2.py — Task 54-35: OP NEW 196571/196605/196596 (Колизей-волна) + хвосты 196475/196562.''',
     '''# rescan54_36b_phase2.py — Task 54-36: OP NEW 196470/196606 (колизей-срыв/издевается) + хвосты 196469/196530.'''),

    ('''for tid in (196571, 196605, 196596):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)
    summary(tid, '1', head_n=3, tail_n=4)
for tid in (196475, 196562):''',
     '''for tid in (196470, 196606):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)
    summary(tid, '1', head_n=3, tail_n=4)
for tid in (196469, 196530):'''),
]

out = open(SRC, encoding='utf-8').read()
for i, (old, new) in enumerate(REPL, 1):
    if old not in out:
        sys.exit(f'PATTERN NOT FOUND ({i}/{len(REPL)}): {old[:90]!r}')
    out = out.replace(old, new, 1)
open(DST, 'w', encoding='utf-8').write(out)
py_compile.compile(DST, doraise=True)
print(f'OK {DST} — {len(REPL)}/{len(REPL)} REPL, py_compile OK')
