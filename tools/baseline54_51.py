#!/usr/bin/env python3
# baseline54_51.py — база «был cc=» для меток gen54_51: последние снапшоты discussion_*_near999999_* по каждому tid (из раунда 54-50, TS ~0228).
import os, json, re

OUT = '/home/z/my-project/output/evidence_post'
TIDS = [196452, 196488, 196480, 196511, 196524, 196475, 196522, 196523, 196411,
        196532, 196536, 196533, 196537, 196539, 196424, 196425, 196461, 196435,
        196510, 196520, 196499, 196516, 196513, 196531, 196496, 196260, 196428,
        196078, 196062, 196315, 196415, 196283, 196620, 196623, 196612, 196618,
        196611, 187993, 196572, 196434, 195080, 196561, 196621, 196624, 196619, 196100,
        196625, 196626, 196627, 196628, 196629, 196610, 196552, 196617]

for tid in TIDS:
    best = None
    for fn in os.listdir(OUT):
        m = re.match(rf'discussion_{tid}_near999999_(\d{{8}}_\d{{4}})\.json$', fn)
        if m and (best is None or m.group(1) > best[0]):
            best = (m.group(1), fn)
    if not best:
        print(f'{tid}: NO SNAP'); continue
    try:
        d = json.load(open(os.path.join(OUT, best[1])))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        print(f"{tid}: cc={aa.get('commentCount')} LPN={aa.get('lastPostNumber')} TS={best[0]}")
    except Exception as e:
        print(f'{tid}: ERR {e}')
