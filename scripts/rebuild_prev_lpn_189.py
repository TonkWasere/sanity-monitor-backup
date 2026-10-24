#!/usr/bin/env python3
# rebuild_prev_lpn_189.py — восстановление /tmp/prev_lpn_189.json после WIPE-14/15
# База = git-снапы раунда 54-188 (TS 20261024_0320, закоммичены в ee648b81).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
DST = '/tmp/prev_lpn_189.json'
TS = '20261024_0320'

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
print(f'>>> prev_lpn_189.json восстановлен: {len(state)} ключей (ожидалось ~110)')

# Сверка с контрольными точками из ledger №228 (03:28 UTC):
expect = {196889: (75, 71), 196902: (27, 27), 196918: (10, 9), 196926: (24, 24), 196935: (5, 5), 196936: (3, 3), 196937: (4, 4)}
bad = []
for tid, (lpn, cc) in expect.items():
    got = state.get(str(tid), {})
    if got.get('lpn') != lpn or got.get('cc') != cc:
        bad.append((tid, got, (lpn, cc)))
print('сверка ledger №228:', 'OK все 7 точек' if not bad else f'РАСХОЖДЕНИЯ: {bad}')
