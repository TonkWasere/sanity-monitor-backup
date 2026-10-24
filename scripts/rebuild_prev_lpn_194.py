#!/usr/bin/env python3
# rebuild_prev_lpn_194.py — восстановление /tmp/prev_lpn_194.json после WIPE-23
# База = git-снапы раунда 54-193 (TS 20261024_0820, закоммичены в c54fa1a4).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
DST = '/tmp/prev_lpn_194.json'
TS = '20261024_0820'

state = {}
for fn in sorted(os.listdir(OUT)):
    m = re.match(r'discussion_(\d+)_near999999_' + TS + r'\.json', fn)
    if not m:
        continue
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        tid = int(m.group(1))
        state[str(tid)] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'SKIP {fn}: {e}')

json.dump(state, open(DST, 'w'))
print(f'>>> prev_lpn_194.json восстановлен: {len(state)} ключей (ожидалось ~119)')

# Сверка с контрольными точками из ledger №233 (08:2x UTC, дельты 54-193):
expect = {196943: (41, 40), 196935: (42, 38), 196907: (72, 69), 196946: (15, 15), 196944: (6, 6), 196945: (1, 1), 196942: (9, 9), 196936: (18, 18), 196928: (19, 19), 112917: (67767, 66514)}
bad = []
for tid, (lpn, cc) in expect.items():
    got = state.get(str(tid), {})
    if got.get('lpn') != lpn or got.get('cc') != cc:
        bad.append((tid, got, (lpn, cc)))
print('сверка ledger №233:', f'OK все {len(expect)} точек' if not bad else f'РАСХОЖДЕНИЯ: {bad}')
