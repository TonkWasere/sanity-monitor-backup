#!/usr/bin/env python3
# rebuild_prev_lpn_208.py — WIPE-37 (27-й откат): восстановление /tmp/prev_lpn_208.json
# из git-снапов near999999 20261024_2220 (база 54-207, 22:20-22:29 UTC, ff 403618ed)
# + lite-надстройка 22:25 (196976 7/7 — дельта SNAP15 RECONCILE-ADD после закрытия
# 54-207). Эталон: ledger №247 (150 кл, 0 NEW).
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_2220.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_2220\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        lpn, cc = aa.get('lastPostNumber'), aa.get('commentCount')
        if lpn is None:
            continue
        cur[int(m.group(1))] = {'lpn': lpn, 'cc': cc}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

print(f'>>> база TS2220: {len(cur)} ключей')

# Контроль базы TS2220 против эталона №247 (значения на 22:2x)
checks_ts = {
    196972: (37, 37),    # stm-баланс 5-й срез 15→20→27→29→35→37
    196973: (23, 23),    # худший игрок +2
    196975: (22, 22),    # арбитр замер
    196974: (13, 13),    # фидбек арены замер
    196976: (6, 6),      # «Халява прийдёт» (lite догонит до 7)
    196977: (2, 2),      # NEW 21:05, не развился
    196979: (2, 2),      # NEW 21:50 «калибровка»
    196939: (25, 24),    # «Сборояка на кровоток» +7, гэп 1
    196956: (16, 15),    # вырез-подозрение, гэп 1
    191614: (7379, 7315),  # кот-тред +6
    196875: (81, 81),    # колизей +3
    196927: (36, 36),    # «Очередная халтура» ожил +1
    196949: (43, 43),    # +1
    196959: (29, 27),    # +1
    196970: (12, 12),    # +1
    196943: (183, 181),  # замер
    196902: (69, 69),    # замер
    196834: (64, 57),    # гэп 7
    196899: (9, 9),      # замер
    196969: (15, 15),    # замер
    196971: (7, 7),      # замер
    196968: (41, 41),    # замер
    196952: (36, 36),    # замер
    196967: (12, 11),    # вылеты, гэп 1
    196424: (165, 160),  # ОТС тихая линия
}
ok = miss = 0
for tid, (lpn, cc) in checks_ts.items():
    v = cur.get(tid)
    if not v:
        print(f'  MISS {tid}'); miss += 1; continue
    good = v['lpn'] == lpn and v['cc'] == cc
    ok += good
    if not good:
        print(f'  MISMATCH {tid}: {v} ожидалось lpn={lpn} cc={cc}')
print(f'>>> контроль базы TS2220: {ok}/{len(checks_ts)} совпали, miss={miss}')

# Lite-надстройка (SNAP15 22:25 — новее базы; 22:45/22:55 без дельт, 23:10 skipped WIPE-37)
lite = {
    196976: {'lpn': 7, 'cc': 7},  # «Халява прийдёт» 6→7 (SNAP15 22:25 RECONCILE-ADD)
}
for tid, v in lite.items():
    old = cur.get(tid)
    cur[tid] = v
    print(f'  lite-надстройка {tid}: {old} → {v}')
json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_208.json', 'w'))
print(f'>>> prev_lpn_208.json восстановлен: {len(cur)} ключей (lite-надстройка ×{len(lite)})')
