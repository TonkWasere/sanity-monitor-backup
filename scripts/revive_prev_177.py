#!/usr/bin/env python3
# revive_prev_177.py — WIPE-15 recovery (8-й откат): /tmp/prev_lpn_* снова снесены;
# реанимация базы 15:30 UTC 23.10 из TS1530-снапов раунда 54-176 (ушли в remote до отката).
# Результат: /tmp/prev_lpn_177.json (база 15:30 для Task 54-177, окно 15:30→16:30, 1 ч).
# Ожидание: 83 ключа (как в 54-176: prev_lpn_177 83 keys).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
TS = '20261023_1530'
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

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_177.json', 'w'))
print(f'prev_lpn_177.json: {len(cur)} ключей (база 15:30 UTC 23.10, реанимация из TS{TS})')
sanity = {196887: 239, 196834: 47, 196894: 58, 196874: 43, 196898: 19, 196902: 12,
          196903: 19, 196904: 16, 196905: 26, 196906: 6, 196867: 40, 196875: 46,
          196852: 9, 196424: 160, 196888: 16, 196890: 24, 196896: 24}
ok = 0
for t, cc_e in sanity.items():
    v = cur.get(t)
    if v is None:
        print(f'  sanity [{t}]: ОТСУТСТВУЕТ!')
    elif cc_e is not None and v.get('cc') != cc_e:
        print(f"  sanity [{t}]: cc={v.get('cc')} ожидалось {cc_e}")
    else:
        ok += 1
print(f'sanity: {ok}/{len(sanity)} OK')
