#!/usr/bin/env python3
# rebuild_prev_lpn_197.py — WIPE-26: восстановление /tmp/prev_lpn_197.json
# из git-снапов near999999 20261024_1120 (база 54-196, 11:21-11:3x UTC).
# Эталон: ledger №236 «PREV_LPN: /tmp/prev_lpn_197.json 129 ключей».
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_1120.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_1120\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        cur[int(m.group(1))] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_197.json', 'w'))
print(f'>>> prev_lpn_197.json восстановлен: {len(cur)} ключей (эталон №236: 129)')

# Контрольные точки против ledger №236 (значения на 11:2x)
checks = {
    196943: (101, 99),   # «Рейтинг празднества» 4-я волна +24
    196954: (13, 13),    # «Так алё я не понял» NEW stm-OP
    196948: (25, 25),    # «бюджетную связку видюха+проц»
    196949: (27, 27),    # «нерфят арт»
    196950: (3, 3),      # «Проблема с отс» stm
    196951: (13, 13),    # young-взрыв 13/13
    196952: (21, 21),    # «Баланс с отс» stm-OP
    196953: (11, 11),    # «IWI Tavor»
    196907: (80, 76),    # ОТС-фидбек 6-я волна
    196778: (60, 58),    # Цепь Распада (WATCH)
    196889: (85, 81),    # клиент-реквесты (пауза сломана)
    131836: (193, 186),  # офиц. тред распределения
    196411: (90, 85),    # мета-тред заморожен 34 ч+
    196424: (165, 160),  # ОТС ~163 ч
    196452: (30, 30),    # флешмоб талонов ~125-й
    191614: (7351, 7288),  # кот-тред
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
