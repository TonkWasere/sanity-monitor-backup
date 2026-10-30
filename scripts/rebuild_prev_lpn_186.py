#!/usr/bin/env python3
# rebuild_prev_lpn_186.py — восстановление /tmp/prev_lpn_186.json после WIPE-11
# База = git-снапы раунда 54-185 (TS 20261024_0020, закоммичены в 9f5d6060):
# для каждого discussion_<tid>_near999999_20261024_0020.json берём
# data.attributes.lastPostNumber/commentCount — ровно то, что сохранял 185-й скрипт.
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
DST = '/tmp/prev_lpn_186.json'
TS = '20261024_0020'

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
print(f'>>> prev_lpn_186.json восстановлен: {len(state)} ключей (ожидалось ~105)')

# Сверка с контрольными точками из ledger №225 (00:29 UTC):
expect = {196926: (23, 23), 196911: (87, 86), 196907: (50, 47), 196889: (72, 68), 196931: (3, 3)}
bad = []
for tid, (lpn, cc) in expect.items():
    got = state.get(str(tid), {})
    if got.get('lpn') != lpn or got.get('cc') != cc:
        bad.append((tid, got, (lpn, cc)))
print('сверка ledger №225:', 'OK все 5 точек' if not bad else f'РАСХОЖДЕНИЯ: {bad}')
