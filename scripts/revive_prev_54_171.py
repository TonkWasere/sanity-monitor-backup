#!/usr/bin/env python3
# revive_prev_54_171.py — реанимация prev_lpn-базы после WIPE-10 (по образцу 54-167).
# База = TS0130-снапы (раунд 54-167, последний выполненный; /tmp снесён откатом ВМ).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
SRC_TS = '20261023_0130'   # база 01:30 UTC (54-167)
DST = '/tmp/prev_lpn_168.json'  # база для окна 01:30→05:30 раунда 54-171

cur = {}
for fn in os.listdir(OUT):
    m = re.match(r'discussion_(\d+)_near999999_' + SRC_TS + r'\.json', fn)
    if not m:
        continue
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        a = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        cur[int(m.group(1))] = {'lpn': a.get('lastPostNumber'), 'cc': a.get('commentCount')}
    except Exception:
        pass

json.dump({str(k): v for k, v in cur.items()}, open(DST, 'w'))
print(f'prev оживлена: {len(cur)} ключей -> {DST} (база {SRC_TS})')
