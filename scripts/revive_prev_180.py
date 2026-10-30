#!/usr/bin/env python3
# revive_prev_180.py — WIPE-16 recovery (9-й откат): /tmp/prev_lpn_* снова снесены;
# реанимация базы 18:30 UTC 23.10 из TS1830-снапов раунда 54-179 (ушли в remote до отката).
# Результат: /tmp/prev_lpn_180.json (база 18:30 для Task 54-180, окно 18:30→19:30, 1 ч).
# Ожидание: 91 ключ (как в 54-179: prev_lpn_180 91 keys).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
TS = '20261023_1830'
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

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_180.json', 'w'))
print(f'prev_lpn_180.json: {len(cur)} ключей (база 18:30 UTC 23.10, реанимация из TS{TS})')
sanity = {196887: 242, 196834: 48, 196894: 58, 196874: 45, 196898: 19, 196902: 16,
          196904: 16, 196905: 25, 196906: 6, 196867: 40, 196875: 57,
          196852: 9, 196424: 160, 196888: 16, 196890: 24, 196896: 24, 196832: 218,
          196889: 51, 196907: 23, 196911: 66, 196913: 17, 196916: 10, 196452: 30}
ok = 0
for t, cc_e in sanity.items():
    v = cur.get(t)
    if v and v.get('cc') == cc_e:
        ok += 1
    else:
        print(f'  SANITY FAIL [{t}]: ожидано cc={cc_e}, факт={v}')
print(f'sanity: {ok}/{len(sanity)} OK')
