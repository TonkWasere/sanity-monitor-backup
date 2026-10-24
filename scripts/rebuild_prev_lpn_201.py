#!/usr/bin/env python3
# rebuild_prev_lpn_201.py — WIPE-30: восстановление /tmp/prev_lpn_201.json
# из git-снапов near999999 20261024_1520 (база 54-200, 15:21-15:33 UTC).
# Эталон: ledger №240 «PREV_LPN: /tmp/prev_lpn_201.json 137 ключей».
# ВАЖНО: 196967 в снапах 1520 ОТСУТСТВУЕТ (рождён 14:57, но в WATCH 54-200 не
# входил; пойман SNAP35 15:36) — в 54-201 будет «ЛИН/НЕТ В PREV», это штатно.
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_1520.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_1520\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        cur[int(m.group(1))] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_201.json', 'w'))
print(f'>>> prev_lpn_201.json восстановлен: {len(cur)} ключей (эталон №240: 137)')

# Контрольные точки против ledger №240 (значения на 15:2x)
checks = {
    196966: (9, 7),      # NEW офиц. патчноут ОТС (11/9 пришёл позже, SNAP15 15:40)
    196965: (13, 13),    # NEW ОТС-тех
    196964: (2, 2),      # NEW stm-твинк
    196962: (1, 1),      # NEW stm-твинк
    196943: (153, 151),  # 8-я волна +6, гэп 2
    196907: (101, 97),   # фидбек 2-й час +9, гэп 4
    196889: (95, 91),    # старт ОТС +1
    196902: (54, 54),    # Замок Сефиры +2
    196946: (40, 40),    # 8-й час
    196949: (38, 38),    # нерф-тред +4
    196875: (73, 73),    # петиция колизея +6
    196952: (32, 32),    # stm-OP ожил +4
    196955: (10, 10),    # ожил +2
    196953: (21, 21),
    196960: (13, 13),
    196959: (15, 13),    # гэп 2
    196927: (17, 17),    # +6
    196948: (30, 30),
    196834: (57, 50),    # Арты Шурика
    196894: (64, 61),    # гэп 3
    196936: (22, 22),
    196945: (4, 4),
    191614: (7359, 7296),  # кот-тред +4
    112917: (67780, 66527),  # мегатред +2
    196411: (90, 85),    # заморожен 38 ч
    196424: (165, 160),  # ОТС ~167 ч
    196425: (132, 125),
    196452: (30, 30),    # флешмоб 129-й
    196488: (48, 45),    # кейс ~175 ч
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
for tid, (lpn, cc) in checks.items():
    v = cur.get(tid)
    if not v:
        print(f'  MISS {tid}'); miss += 1; continue
    good = v['lpn'] == lpn and v['cc'] == cc
    ok += good
    if not good:
        print(f'  MISMATCH {tid}: {v} ожидалось lpn={lpn} cc={cc}')
print(f'>>> контроль: {ok}/{len(checks)} совпали, miss={miss}')
