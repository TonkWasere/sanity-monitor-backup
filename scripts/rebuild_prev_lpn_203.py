#!/usr/bin/env python3
# rebuild_prev_lpn_203.py — WIPE-32 (22-й откат): восстановление /tmp/prev_lpn_203.json
# из git-снапов near999999 20261024_1720 (база 54-202, 17:20-17:36 UTC, ff 28864dd0)
# + lite-надстройка SNAP15 17:42 (196968 39/39 — последняя lite-дельта до WIPE-32).
# Эталон: ledger №242.
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_1720.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_1720\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        cur[int(m.group(1))] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

print(f'>>> база TS1720: {len(cur)} ключей')

# Контроль базы TS1720 против эталона №242 (значения на 17:2x)
checks_ts = {
    196943: (171, 169),  # 10-я волна +12, гэп 2
    196902: (68, 68),    # всплеск +13
    196927: (31, 31),    # +9
    196968: (39, 39),    # 4-й срез разгона
    196966: (21, 19),    # гэп 2
    196946: (53, 53),    # 10-й час
    196964: (6, 6),
    196865: (48, 48),    # Crios dev-ответ #47
    196899: (3, 3),      # ожил на фронт
    196907: (103, 99),
    196889: (95, 91),
    196902: (68, 68),
    196959: (20, 18),
    196960: (13, 13),
    196965: (13, 13),
    196967: (11, 10),
    196952: (33, 33),
    196948: (33, 33),
    196949: (42, 42),
    196875: (74, 74),
    196834: (57, 50),
    196890: (25, 25),
    196894: (65, 62),
    196832: (227, 227),
    196926: (35, 35),
    196936: (24, 24),
    196945: (5, 5),
    196856: (50, 48),
    196838: (45, 42),
    196872: (29, 29),
    196855: (25, 25),
    196854: (96, 95),
    196867: (42, 42),
    191614: (7363, 7300),
    112917: (67785, 66532),
    196411: (90, 85),
    196424: (165, 160),
    196425: (132, 125),
    196452: (30, 30),
    196488: (48, 45),
    196480: (172, 171),
    196778: (60, 58),
    131836: (193, 186),
    196918: (13, 12),
    196919: (9, 8),
    196922: (10, 10),
    196923: (13, 13),
    196924: (9, 9),
    196925: (12, 11),
    196930: (14, 14),
    196954: (13, 13),
    196956: (6, 6),
    196913: (19, 19),
    196917: (7, 7),
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
print(f'>>> контроль базы TS1720: {ok}/{len(checks_ts)} совпали, miss={miss}')

# Lite-надстройка (SNAP15 17:42 — новее базы)
lite = {
    196968: {'lpn': 39, 'cc': 39},   # 17:42 RECONCILE-ADD 39/39
}
for tid, v in lite.items():
    old = cur.get(tid)
    cur[tid] = v
    print(f'  lite-надстройка {tid}: {old} → {v}')
json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_203.json', 'w'))
print(f'>>> prev_lpn_203.json восстановлен: {len(cur)} ключей (lite-надстройка ×{len(lite)})')
