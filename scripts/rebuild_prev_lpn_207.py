#!/usr/bin/env python3
# rebuild_prev_lpn_207.py — WIPE-36 (26-й откат): восстановление /tmp/prev_lpn_207.json
# из git-снапов near999999 20261024_2120 (база 54-206, 21:20-21:39 UTC, ff 5013707a)
# + lite-надстройки 21:40/21:55 (196973 21/21, 196976 6/6, 196979 2/2 — дельты
# SNAP15 + RECONCILE-ADD после закрытия 54-206). Эталон: ledger №246 (149 кл + 1 NEW).
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_2120.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_2120\.json', os.path.basename(fn))
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

print(f'>>> база TS2120: {len(cur)} ключей')

# Контроль базы TS2120 против эталона №246 (значения на 21:2x)
checks_ts = {
    196977: (2, 2),      # NEW 21:05 «Stalzone удаляет акк» BeerokSC
    196976: (4, 4),      # «Халява прийдёт» (lite догонит до 6)
    196975: (22, 22),    # арбитр stm 3-й срез слабый
    196974: (13, 13),    # фидбек арены
    196973: (20, 20),    # худший игрок (lite догонит до 21)
    196972: (35, 35),    # stm-баланс 4-й срез 15→20→27→29→35
    196875: (78, 78),    # колизей +4
    196838: (48, 45),    # арена Митрополита +3, гэп 3
    191614: (7373, 7309),    # кот-тред +3
    112917: (67797, 66544),  # мегатред +1
    196952: (36, 36),
    196968: (41, 41),    # «И куда?» +2
    196967: (12, 11),    # вылеты, гэп 1
    196943: (183, 181),  # замер
    196956: (14, 14),    # замер
    196959: (28, 26),
    196902: (69, 69),
    196834: (64, 57),    # гэп 7
    196899: (9, 9),
    196969: (15, 15),
    196424: (165, 160),
    196425: (132, 125),
    196488: (48, 45),
    196480: (172, 171),
    196411: (90, 85),
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
print(f'>>> контроль базы TS2120: {ok}/{len(checks_ts)} совпали, miss={miss}')

# Lite-надстройки (SNAP15 21:40 + 21:55 — новее базы; 22:10 skipped WIPE-36)
lite = {
    196973: {'lpn': 21, 'cc': 21},  # худший игрок 20→21 (SNAP15 21:40)
    196976: {'lpn': 6, 'cc': 6},    # «Халява прийдёт» 4→6 (21:40 +1, 21:55 +1)
    196979: {'lpn': 2, 'cc': 2},    # NEW RECONCILE-ADD 21:55 «калибровка» (21:50 UTC)
}
for tid, v in lite.items():
    old = cur.get(tid)
    cur[tid] = v
    print(f'  lite-надстройка {tid}: {old} → {v}')
json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_207.json', 'w'))
print(f'>>> prev_lpn_207.json восстановлен: {len(cur)} ключей (lite-надстройка ×{len(lite)})')
