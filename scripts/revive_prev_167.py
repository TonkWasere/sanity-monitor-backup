#!/usr/bin/env python3
# revive_prev_167.py — WIPE-10 recovery: /tmp/prev_lpn_* снесены; реанимация базы 23:30 UTC 22.10
# из TS2330-снапов раунда 54-165 (урок: prev из near999999-снапов восстанавливается 100%).
# Результат: /tmp/prev_lpn_167.json (база 23:30 для Task 54-167, окно 23:30→01:30).
# Ожидание: 61 ключ (как prev_lpn_166.json в 54-165).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
TS = '20261022_2330'
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

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_167.json', 'w'))
print(f'prev_lpn_167.json: {len(cur)} ключей (база 23:30 UTC 22.10, реанимация из TS{TS})')
sanity = {193924: (67, 68), 196852: (9, 10), 196875: (26, None), 196873: (23, 24), 196867: (27, None)}
for t, (cc_e, lpn_e) in sanity.items():
    v = cur.get(t)
    print(f'  sanity [{t}]: lpn={v["lpn"]} cc={v["cc"]}' if v else f'  sanity [{t}]: ОТСУТСТВУЕТ!')
