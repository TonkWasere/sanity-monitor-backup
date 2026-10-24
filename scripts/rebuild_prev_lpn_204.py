#!/usr/bin/env python3
# rebuild_prev_lpn_204.py — WIPE-33 (23-й откат): восстановление /tmp/prev_lpn_204.json
# из git-снапов near999999 20261024_1820 (база 54-203, 18:20-18:29 UTC, ff 2a7ca6a3)
# + lite-надстройка SNAP15 18:40 (196969 9/9 — последняя lite-дельта до WIPE-33).
# Эталон: ledger №243 (140 ключей, 12 дельт-сущностей).
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_1820.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_1820\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        cur[int(m.group(1))] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

print(f'>>> база TS1820: {len(cur)} ключей')

# Контроль базы TS1820 против эталона №243 (значения на 18:2x)
checks_ts = {
    196943: (181, 179),  # 11-я волна +10, гэп 2
    196899: (9, 9),      # +6 колизей-вопрос
    196927: (35, 35),    # +4, 3-й час разгона
    196962: (3, 3),      # stm «Статус стим» +2
    196948: (36, 36),    # +3
    196907: (104, 100),  # оттепель +1
    112917: (67788, 66535),  # мегатред +3
    191614: (7366, 7303),    # кот-тред +3
    196834: (59, 52),    # +2
    196832: (229, 229),  # +2
    196959: (21, 19),    # +1, гэп 2
    196894: (66, 63),    # +1
    196968: (39, 39),    # замер после разгона
    196902: (68, 68),    # всплеск +13 отработал
    196966: (21, 19),    # патчноут, гэп 2
    196946: (53, 53),    # 10-й час отработал
    196424: (165, 160),  # ОТС
    196425: (132, 125),  # ОТС сбор
    196488: (48, 45),    # кейс
    196480: (172, 171),  # компенсация
    196411: (90, 85),    # мета-тред заморожен 41ч
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
print(f'>>> контроль базы TS1820: {ok}/{len(checks_ts)} совпали, miss={miss}')

# Lite-надстройка (SNAP15 18:40 — новее базы; SNAP15 18:55/19:10 skipped WIPE-33)
lite = {
    196969: {'lpn': 9, 'cc': 9},   # 18:40 молодой: 1/1→9/9 активный рост
}
for tid, v in lite.items():
    old = cur.get(tid)
    cur[tid] = v
    print(f'  lite-надстройка {tid}: {old} → {v}')
json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_204.json', 'w'))
print(f'>>> prev_lpn_204.json восстановлен: {len(cur)} ключей (lite-надстройка ×{len(lite)})')
