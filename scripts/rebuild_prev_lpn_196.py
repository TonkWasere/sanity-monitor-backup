#!/usr/bin/env python3
# rebuild_prev_lpn_196.py — WIPE-25: восстановление /tmp/prev_lpn_196.json
# из git-снапов near999999 20261024_1020 (база 54-195, 10:24-10:32 UTC).
# Эталон: ledger №235 «PREV_LPN: /tmp/prev_lpn_196.json 126 ключей».
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_1020.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_1020\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        cur[int(m.group(1))] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_196.json', 'w'))
print(f'>>> prev_lpn_196.json восстановлен: {len(cur)} ключей')

# Контрольные точки против ledger №235 (значения на 10:2x)
checks = {
    196943: (77, 75),   # «Рейтинг празднества» 3-я волна +28
    196948: (18, 18),   # «бюджетную связку видюха+проц» +14
    196949: (25, 25),   # «нерфят арт» замедлился
    196946: (26, 26),   # «распреду» 3-й час
    196907: (77, 74),   # ОТС-фидбек +1
    196875: (64, 64),   # Колизей-кластер
    196935: (42, 38),   # ивент-тред (2-я пауза)
    196889: (84, 80),   # клиент-реквесты (3-я пауза)
    131836: (193, 186), # офиц. тред распределения
    196778: (59, 57),   # Цепь Распада (WATCH добор)
    196411: (90, 85),   # заморожен 33 ч+
    196424: (165, 160), # ОТС 162 ч
    196452: (30, 30),   # флешмоб талонов 124-й
    191614: (7350, 7288),  # кот-тред
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
print(f'контроль: {ok}/{len(checks)} OK, miss={miss}')
