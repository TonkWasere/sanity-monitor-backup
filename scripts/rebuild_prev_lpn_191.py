#!/usr/bin/env python3
# rebuild_prev_lpn_191.py — восстановление /tmp/prev_lpn_191.json после WIPE-18
# База = git-снапы раунда 54-190 (TS 20261024_0520, закоммичены в 6396ea6b).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
DST = '/tmp/prev_lpn_191.json'
TS = '20261024_0520'

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
print(f'>>> prev_lpn_191.json восстановлен: {len(state)} ключей (ожидалось ~111)')

# Сверка с контрольными точками из ledger №230 (05:2x UTC):
expect = {196938: (15, 15), 196937: (11, 10), 196936: (11, 11), 196889: (79, 75), 196926: (28, 28), 196842: (58, 58), 196935: (7, 6), 196905: (31, 29), 196902: (29, 29), 196928: (11, 11)}
bad = []
for tid, (lpn, cc) in expect.items():
    got = state.get(str(tid), {})
    if got.get('lpn') != lpn or got.get('cc') != cc:
        bad.append((tid, got, (lpn, cc)))
print('сверка ledger №230:', f'OK все {len(expect)} точек' if not bad else f'РАСХОЖДЕНИЯ: {bad}')
