#!/usr/bin/env python3
# revive_prev_170.py — WIPE-13 recovery (6-й откат): /tmp/prev_lpn_* снова снесены;
# реанимация базы 08:30 UTC 23.10 из TS0830-снапов раунда 54-169 (ушли в remote до отката).
# Результат: /tmp/prev_lpn_170.json (база 08:30 для Task 54-170, окно 08:30→09:30, 1 ч).
# Ожидание: 68 ключей (как в 54-169: prev_lpn_170 68 keys).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
TS = '20261023_0830'
cur = {}
for fn in sorted(os.listdir(OUT)):
    m = re.match(r'discussion_(\d+)_near999999_' + TS + r'\.json', fn)
    if not m:
        continue
    try:
        dd = json.load(open(os.path.join(OUT, fn)))
        aa = dd.get('data', {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
        tid = int(m.group(1))
        cur[tid] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_170.json', 'w'))
print(f'prev_lpn_170.json: {len(cur)} ключей (база 08:30 UTC 23.10, реанимация из TS{TS})')
sanity = {196887: 73, 196832: 196, 196875: 46, 196872: 29, 196873: 27, 196867: 35,
          196877: 20, 196879: 8, 196852: 10, 193924: 68, 196888: None, 196890: None, 196891: None}
for t, cc_e in sanity.items():
    v = cur.get(t)
    if v is None:
        print(f'  sanity [{t}]: ОТСУТСТВУЕТ!')
    elif cc_e is None:
        print(f'  sanity [{t}]: lpn={v["lpn"]} cc={v["cc"]} (новый 54-169, значение не задано)')
    else:
        print(f'  sanity [{t}]: lpn={v["lpn"]} cc={v["cc"]} (ожидался cc≈{cc_e})')
