#!/usr/bin/env python3
# revive_prev_168.py — WIPE-11 recovery: /tmp/prev_lpn_* снесены; реанимация базы 01:30 UTC 23.10
# из TS0130-снапов раунда 54-167 (урок: prev из near999999-снапов восстанавливается 100%).
# Результат: /tmp/prev_lpn_168.json (база 01:30 для Task 54-168, окно 01:30→07:30, ГЭП 6 ч).
# Ожидание: 63 ключа (как prev_lpn_168.json в 54-167: 61 + 196877 + 196879).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
TS = '20261023_0130'
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

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_168.json', 'w'))
print(f'prev_lpn_168.json: {len(cur)} ключей (база 01:30 UTC 23.10, реанимация из TS{TS})')
sanity = {193924: 68, 196875: 30, 196873: 27, 196867: 31, 196877: 5, 196879: 7, 196852: 10, 196832: 110}
for t, cc_e in sanity.items():
    v = cur.get(t)
    print(f'  sanity [{t}]: lpn={v["lpn"]} cc={v["cc"]} (ожидался cc≈{cc_e})' if v else f'  sanity [{t}]: ОТСУТСТВУЕТ!')
