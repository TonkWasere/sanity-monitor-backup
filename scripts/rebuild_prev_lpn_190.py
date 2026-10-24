#!/usr/bin/env python3
# rebuild_prev_lpn_190.py — восстановление /tmp/prev_lpn_190.json после WIPE-16/17
# База = git-снапы раунда 54-189 (TS 20261024_0420, закоммичены в 7a8a7831).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
DST = '/tmp/prev_lpn_190.json'
TS = '20261024_0420'

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
print(f'>>> prev_lpn_190.json восстановлен: {len(state)} ключей (ожидалось ~111)')

# Сверка с контрольными точками из ledger №229 (04:28 UTC):
expect = {196938: (14, 14), 191614: (7349, 7287), 196889: (77, 73), 196907: (57, 54), 196937: (10, 9), 196935: (7, 7), 196936: (5, 5)}
bad = []
for tid, (lpn, cc) in expect.items():
    got = state.get(str(tid), {})
    if got.get('lpn') != lpn or got.get('cc') != cc:
        bad.append((tid, got, (lpn, cc)))
print('сверка ledger №229:', 'OK все 7 точек' if not bad else f'РАСХОЖДЕНИЯ: {bad}')
