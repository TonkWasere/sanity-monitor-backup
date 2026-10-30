#!/usr/bin/env python3
# rebuild_prev_lpn_200.py — WIPE-29: восстановление /tmp/prev_lpn_200.json
# из git-снапов near999999 20261024_1420 (база 54-199, 14:21-14:32 UTC).
# Эталон: ledger №239 «PREV_LPN: /tmp/prev_lpn_200.json 133 ключей».
# ВАЖНО: 196962/196964/196965 в снапах 1420 ОТСУТСТВУЮТ (рождены 14:01/14:27/14:29,
# пойманы SNAP35 14:38 после закрытия окна) — в 54-200 будет «НЕТ В PREV», это штатно.
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_1420.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_1420\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        cur[int(m.group(1))] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_200.json', 'w'))
print(f'>>> prev_lpn_200.json восстановлен: {len(cur)} ключей (эталон №239: 133)')

# Контрольные точки против ledger №239 (значения на 14:2x)
checks = {
    196943: (147, 145),  # 7-я волна +13, гэп 2
    196907: (92, 88),    # фидбек-вспышка +11, гэп 4
    196889: (94, 90),    # старт ОТС 2-й час, Aidka #91
    196902: (52, 52),    # Замок Сефиры замер
    196946: (39, 39),    # 7-й час +4
    196949: (34, 34),    # нерф-тред +4
    196953: (20, 20),    # IWI Tavor +3
    196959: (15, 13),    # young замер, гэп 2
    196960: (12, 12),    # young (SNAP15 14:40 показал 13/13 — уже после окна)
    196955: (8, 8),
    196954: (13, 13),
    196956: (6, 6),
    196952: (28, 28),
    196948: (28, 28),
    196875: (67, 67),
    196894: (63, 60),    # гэп 3
    196913: (19, 19),
    196917: (7, 7),
    196918: (13, 12),    # гэп 1, Aidka #13
    196919: (9, 8),      # гэп 1
    196922: (10, 10),
    196923: (13, 13),
    196924: (9, 9),
    196925: (11, 10),    # гэп 1
    196926: (34, 34),
    196927: (11, 11),
    196930: (14, 14),
    196778: (60, 58),
    131836: (193, 186),
    196411: (90, 85),    # заморожен 37 ч
    196424: (165, 160),  # ОТС ~166 ч
    196425: (132, 125),
    196452: (30, 30),    # флешмоб 128-й
    196488: (48, 45),    # кейс ~174 ч
    196480: (172, 171),
    191614: (7355, 7292),  # кот-тред +1
    112917: (67778, 66525),  # мегатред +3
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
