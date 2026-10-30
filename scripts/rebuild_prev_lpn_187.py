#!/usr/bin/env python3
# rebuild_prev_lpn_187.py — восстановление /tmp/prev_lpn_187.json после WIPE-12
# База = git-снапы раунда 54-186 (TS 20261024_0120, закоммичены в c53d2c1a):
# для каждого discussion_<tid>_near999999_20261024_0120.json берём
# data.attributes.lastPostNumber/commentCount — ровно то, что сохранял 186-й скрипт.
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
DST = '/tmp/prev_lpn_187.json'
TS = '20261024_0120'

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
print(f'>>> prev_lpn_187.json восстановлен: {len(state)} ключей (ожидалось ~105)')

# Сверка с контрольными точками из ledger №226 (01:42 UTC):
expect = {196889: (74, 70), 196907: (53, 50), 196874: (63, 61), 196905: (30, 28), 196877: (23, 23), 196931: (4, 4)}
bad = []
for tid, (lpn, cc) in expect.items():
    got = state.get(str(tid), {})
    if got.get('lpn') != lpn or got.get('cc') != cc:
        bad.append((tid, got, (lpn, cc)))
print('сверка ledger №226:', 'OK все 6 точек' if not bad else f'РАСХОЖДЕНИЯ: {bad}')
