#!/usr/bin/env python3
# rebuild_prev_lpn_193.py — восстановление /tmp/prev_lpn_193.json после WIPE-21
# База = git-снапы раунда 54-192 (TS 20261024_0720, закоммичены в ddcbc61b).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
DST = '/tmp/prev_lpn_193.json'
TS = '20261024_0720'

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
print(f'>>> prev_lpn_193.json восстановлен: {len(state)} ключей (ожидалось ~116)')

# Сверка с контрольными точками из ledger №232 (07:2x UTC):
expect = {196935: (23, 22), 196936: (15, 15), 196889: (84, 80), 196943: (4, 4), 196941: (4, 3), 196942: (6, 6), 196939: (9, 9), 196940: (4, 4), 196928: (14, 14), 191614: (7350, 7288)}
bad = []
for tid, (lpn, cc) in expect.items():
    got = state.get(str(tid), {})
    if got.get('lpn') != lpn or got.get('cc') != cc:
        bad.append((tid, got, (lpn, cc)))
print('сверка ledger №232:', f'OK все {len(expect)} точек' if not bad else f'РАСХОЖДЕНИЯ: {bad}')
