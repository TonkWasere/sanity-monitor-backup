#!/usr/bin/env python3
# rebuild_prev_lpn_195.py — WIPE-24: восстановление /tmp/prev_lpn_195.json
# из git-снапов near999999 20261024_0920 (база 54-194, 09:20-09:29 UTC).
# Эталон: ledger №234 «PREV_LPN: /tmp/prev_lpn_195.json 123 ключа».
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_0920.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_0920\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        cur[int(m.group(1))] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_195.json', 'w'))
print(f'>>> prev_lpn_195.json восстановлен: {len(cur)} ключей')

# Контрольные точки против ledger №234 (значения на 09:2x)
checks = {
    196946: (24, 24),   # «распреду» +9
    196943: (49, 48),   # «Рейтинг празднества»
    196929: (14, 14),   # ностальгия +10
    196907: (76, 73),   # ОТС-фидбек
    196935: (42, 38),   # ивент-тред (пауза)
    196889: (84, 80),   # клиент-реквесты
    196949: (22, 22),   # «нерфят арт»
    131836: (193, 186), # офиц. тред распределения
    196778: (59, 57),   # Цепь Распада (добран разовым фетчем 09:3x)
    112917: (67769, 66516),  # мегатред
    196411: (90, 85),   # заморожен
    196424: (165, 160), # ОТС
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
