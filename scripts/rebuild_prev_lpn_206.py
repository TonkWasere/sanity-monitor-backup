#!/usr/bin/env python3
# rebuild_prev_lpn_206.py — WIPE-35 (25-й откат): восстановление /tmp/prev_lpn_206.json
# из git-снапов near999999 20261024_2020 (база 54-205, 20:20-20:31 UTC, ff 79c943a0)
# + lite-надстройки 20:25/20:40 (196975 21/21, 196973 12/12, 196972 29/29, 196976 2/2 —
# дельты SNAP15 + RECONCILE-ADD после закрытия 54-205; lite 20:55/21:10 skipped WIPE-35).
# Эталон: ledger №245 (147 кл + 1 NEW 196975).
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_2020.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_2020\.json', os.path.basename(fn))
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

print(f'>>> база TS2020: {len(cur)} ключей')

# Контроль базы TS2020 против эталона №245 (значения на 20:2x)
checks_ts = {
    196975: (17, 17),    # NEW 19:51 арбитр stm-твинк
    196972: (27, 27),    # stm-баланс 3-й срез 15→20→27
    196973: (10, 10),    # stm худший игрок
    196974: (12, 12),    # фидбек арены (OP Kikizo)
    196971: (7, 7),      # stm-твинк замер
    196970: (11, 11),    # шитпост замер
    196956: (14, 14),    # не-stm разгон +8
    196943: (183, 181),  # рейтинг празднества замер (hot кончился)
    196959: (28, 26),    # +1, гэп 2
    196902: (69, 69),    # 2-я волна не случилась
    196924: (12, 12),
    196952: (34, 34),
    196834: (64, 57),    # гэп 7
    196969: (15, 15),    # молодой 2-й час
    196899: (9, 9),      # колизей-вопрос
    196927: (35, 35),
    196968: (39, 39),
    196946: (53, 53),
    196948: (39, 39),
    196966: (22, 20),    # патчноут
    112917: (67796, 66543),  # мегатред +4
    191614: (7370, 7306),    # кот-тред +4
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
print(f'>>> контроль базы TS2020: {ok}/{len(checks_ts)} совпали, miss={miss}')

# Lite-надстройки (SNAP15 20:25 + 20:40 — новее базы; 20:55/21:10 skipped WIPE-35)
lite = {
    196975: {'lpn': 21, 'cc': 21},  # арбитр 18→21 (SNAP15 20:40; 20:25 был 18/18)
    196973: {'lpn': 12, 'cc': 12},  # худший игрок 10→12 (SNAP15 20:40)
    196972: {'lpn': 29, 'cc': 29},  # stm-баланс 27→29 (серия 15→20→27→28→29)
    196976: {'lpn': 2, 'cc': 2},    # NEW RECONCILE-ADD 20:40 «Халява прийдёт» (20:36 UTC)
}
for tid, v in lite.items():
    old = cur.get(tid)
    cur[tid] = v
    print(f'  lite-надстройка {tid}: {old} → {v}')
json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_206.json', 'w'))
print(f'>>> prev_lpn_206.json восстановлен: {len(cur)} ключей (lite-надстройка ×{len(lite)})')
