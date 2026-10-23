#!/usr/bin/env python3
# revive_prev_169.py — WIPE-12 recovery: /tmp/prev_lpn_* снесены; реанимация базы 07:30 UTC 23.10
# из TS0730-снапов раунда 54-168 (урок: prev из near999999-снапов восстанавливается 100%).
# Результат: /tmp/prev_lpn_169.json (база 07:30 для Task 54-169, окно 07:30→08:30).
# Ожидание: 65 ключей (как prev_lpn_169.json в 54-168: 63 + 196834 + 196887).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
TS = '20261023_0730'
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

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_169.json', 'w'))
print(f'prev_lpn_169.json: {len(cur)} ключей (база 07:30 UTC 23.10, реанимация из TS{TS})')
sanity = {196832: 190, 196875: 46, 196872: 29, 196867: 33, 196877: 20, 193924: 69, 196834: 18, 196887: 52}
for t, cc_e in sanity.items():
    v = cur.get(t)
    print(f'  sanity [{t}]: lpn={v["lpn"]} cc={v["cc"]} (ожидался cc≈{cc_e})' if v else f'  sanity [{t}]: ОТСУТСТВУЕТ!')
