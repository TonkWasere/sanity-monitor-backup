#!/usr/bin/env python3
# rebuild_prev_lpn_199.py — WIPE-28: восстановление /tmp/prev_lpn_199.json
# из git-снапов near999999 20261024_1320 (база 54-198, 13:21-13:31 UTC).
# Эталон: ledger №238 «PREV_LPN: /tmp/prev_lpn_199.json 133 ключей».
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_1320.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_1320\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        cur[int(m.group(1))] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_199.json', 'w'))
print(f'>>> prev_lpn_199.json восстановлен: {len(cur)} ключей (эталон №238: 133)')

# Контрольные точки против ledger №238 (значения на 13:2x)
checks = {
    196943: (134, 132),  # «Рейтинг празднества» 6-я волна +11
    196902: (52, 52),    # «Замок Сефиры» вспышка +9, Crios-инсайты
    196946: (35, 35),    # «распреду» 6-й час
    196889: (89, 85),    # разморозка +4
    196907: (81, 77),    # разморозился +1
    196959: (15, 13),    # young ливер-rage, гэп 2
    196960: (11, 11),    # NEW stm 12:29
    196953: (17, 17),    # IWI Tavor +3
    196952: (28, 28),    # «Баланс с отс» stm-OP
    196955: (8, 8),
    196954: (13, 13),
    196956: (6, 6),
    196948: (28, 28),    # +3
    196949: (30, 30),    # +2
    196875: (67, 67),    # «Петиция колизея» +3
    196894: (63, 60),    # «Празднество 28.10» гэп 3
    196913: (19, 19),    # +2
    196917: (7, 7),      # +3
    196923: (10, 10),
    196925: (11, 10),    # гэп 1
    196930: (14, 14),
    196778: (60, 58),    # Цепь Распада (без дельт в №238)
    131836: (193, 186),  # офиц. тред распределения
    196411: (90, 85),    # мета-тред заморожен 36 ч
    196424: (165, 160),  # ОТС ~165 ч
    196425: (132, 125),  # сбор ОТС (снап авторитетнее в №238)
    196452: (30, 30),    # флешмоб талонов 127-й
    196488: (48, 45),    # кейс ~173 ч
    196480: (172, 171),  # компенсация
    191614: (7354, 7291),  # кот-тред
    112917: (67775, 66522),  # мегатред вайб +2
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
