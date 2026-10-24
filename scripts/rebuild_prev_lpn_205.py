#!/usr/bin/env python3
# rebuild_prev_lpn_205.py — WIPE-34 (24-й откат): восстановление /tmp/prev_lpn_205.json
# из git-снапов near999999 20261024_1920 (база 54-204, 19:20-19:34 UTC, ff 2c3e450e)
# + lite-надстройки 19:35/19:40 (196974 6/6, 196971 7/7, 196972 20/20 — дельты
# SNAP35/SNAP15 после закрытия 54-204). Эталон: ledger №244 (144 ключа + 3 NEW).
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_1920.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_1920\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        cur[int(m.group(1))] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

print(f'>>> база TS1920: {len(cur)} ключей')

# Контроль базы TS1920 против эталона №244 (значения на 19:2x)
checks_ts = {
    196943: (183, 181),  # 12-я волна +2, затухание
    196899: (9, 9),      # колизей-вопрос
    196927: (35, 35),    # разгон встал
    196969: (15, 15),    # молодой 2-й час разгона
    196959: (27, 25),    # +6, гэп 2
    196948: (39, 39),    # +3
    196834: (63, 56),    # +4, гэп 7
    196435: (158, 158),  # колизей-калибровка +2
    196924: (11, 11),
    196855: (27, 27),
    196966: (22, 20),    # патчноут +1
    196889: (96, 92),
    196907: (105, 101),
    112917: (67792, 66539),  # мегатред +4
    196970: (11, 11),    # NEW шитпост
    196972: (15, 15),    # NEW stm-баланс (lite догонит до 20)
    196973: (2, 2),      # NEW stm
    196902: (68, 68),
    196968: (39, 39),
    196946: (53, 53),
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
print(f'>>> контроль базы TS1920: {ok}/{len(checks_ts)} совпали, miss={miss}')

# Lite-надстройки (SNAP35 19:35 + SNAP15 19:40 — новее базы; 19:55/20:10 skipped WIPE-34)
lite = {
    196974: {'lpn': 6, 'cc': 6},    # NEW 19:27 «Фидбек по арене» (SNAP35 19:35)
    196971: {'lpn': 7, 'cc': 7},    # NEW 18:55 stm-твинк (SNAP35 19:35)
    196972: {'lpn': 20, 'cc': 20},  # stm-баланс 15→20 (SNAP15 19:40)
}
for tid, v in lite.items():
    old = cur.get(tid)
    cur[tid] = v
    print(f'  lite-надстройка {tid}: {old} → {v}')
json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_205.json', 'w'))
print(f'>>> prev_lpn_205.json восстановлен: {len(cur)} ключей (lite-надстройка ×{len(lite)})')
