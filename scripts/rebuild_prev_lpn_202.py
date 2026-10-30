#!/usr/bin/env python3
# rebuild_prev_lpn_202.py — WIPE-31 (21-й откат): восстановление /tmp/prev_lpn_202.json
# из git-снапов near999999 20261024_1620 (база 54-201, 16:20-16:27 UTC, ff 491324d1)
# + lite-надстройка SNAP15 16:34/16:40/16:55 (последние известные значения young-тредов).
# Эталон: ledger №241 + lite-строки 54-16-s15 (восстановлены в worklog).
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_1620.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_1620\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        cur[int(m.group(1))] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

print(f'>>> база TS1620: {len(cur)} ключей')

# Контроль базы TS1620 против эталона №241 (значения на 16:2x)
checks_ts = {
    196968: (28, 28),    # NEW «И куда?» burst, Crios в юзерах
    196966: (15, 13),    # патчноут ОТС +6 (16:40 lite 18/16)
    196967: (11, 10),    # stm-твинк, вылеты
    196943: (159, 157),  # 9-я волна +6, hot 6-й час
    196907: (101, 97),   # фидбек, гэп 4
    196889: (95, 91),    # старт ОТС
    196902: (54, 54),
    196946: (50, 50),    # 9-й час, рекорд +10
    196959: (20, 18),    # гэп 2, young-разгон
    196927: (22, 22),    # +5
    196952: (32, 32),
    196955: (10, 10),
    196953: (21, 21),
    196960: (13, 13),
    196964: (2, 2),      # lite 16:40 → 3/3
    196965: (13, 13),
    196962: (1, 1),      # в 16:34 выпущен по TTL тихо
    196948: (30, 30),
    196949: (38, 38),
    196875: (73, 73),
    196834: (57, 50),
    196894: (64, 61),
    196936: (22, 22),
    196945: (4, 4),
    191614: (7359, 7296),
    112917: (67780, 66527),
    196411: (90, 85),    # заморожен 39-й час
    196424: (165, 160),  # ОТС ~168 ч
    196425: (132, 125),
    196452: (30, 30),    # флешмоб 130-й
    196488: (48, 45),    # кейс
    196480: (172, 171),
    196778: (60, 58),
    131836: (193, 186),
    196918: (13, 12),
    196919: (9, 8),
    196922: (10, 10),
    196923: (13, 13),
    196924: (9, 9),
    196925: (11, 10),
    196926: (34, 34),
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
print(f'>>> контроль базы TS1620: {ok}/{len(checks_ts)} совпали, miss={miss}')

# Lite-надстройка (SNAP15 16:34/16:40/16:55 — новее базы)
lite = {
    196968: {'lpn': 33, 'cc': 33},   # 16:55: 31/31→33/33
    196966: {'lpn': 18, 'cc': 16},   # 16:40: 16/14→18/16
    196967: {'lpn': 11, 'cc': 10},   # 16:55: без дельт
    196965: {'lpn': 13, 'cc': 13},   # 16:55: без дельт
    196964: {'lpn': 3, 'cc': 3},     # 16:40: 2/2→3/3
}
applied = 0
for tid, v in lite.items():
    old = cur.get(tid)
    cur[tid] = v
    applied += 1
    print(f'  lite-надстройка {tid}: {old} → {v}')
json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_202.json', 'w'))
print(f'>>> prev_lpn_202.json восстановлен: {len(cur)} ключей (lite-надстройка ×{applied})')
