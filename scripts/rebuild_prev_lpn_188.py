#!/usr/bin/env python3
# rebuild_prev_lpn_188.py — восстановление /tmp/prev_lpn_188.json после WIPE-13
# База = git-снапы раунда 54-187 (TS 20261024_0220, закоммичены в eceb18b2).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
DST = '/tmp/prev_lpn_188.json'
TS = '20261024_0220'

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
print(f'>>> prev_lpn_188.json восстановлен: {len(state)} ключей (ожидалось ~109)')

# Сверка с контрольными точками из ledger №227 (02:42 UTC):
expect = {191614: (7348, 7286), 196907: (54, 51), 196874: (64, 62), 196935: (3, 3), 196936: (1, 1), 196933: (0, 1), 196934: (0, 1)}
bad = []
for tid, (lpn, cc) in expect.items():
    got = state.get(str(tid), {})
    if got.get('lpn') != lpn or got.get('cc') != cc:
        bad.append((tid, got, (lpn, cc)))
print('сверка ledger №227:', 'OK все 7 точек' if not bad else f'РАСХОЖДЕНИЯ: {bad}')
