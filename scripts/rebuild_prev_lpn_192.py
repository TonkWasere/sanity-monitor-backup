#!/usr/bin/env python3
# rebuild_prev_lpn_192.py — восстановление /tmp/prev_lpn_192.json после WIPE-19
# База = git-снапы раунда 54-191 (TS 20261024_0620, закоммичены в eca37560).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
DST = '/tmp/prev_lpn_192.json'
TS = '20261024_0620'

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
print(f'>>> prev_lpn_192.json восстановлен: {len(state)} ключей (ожидалось ~114)')

# Сверка с контрольными точками из ledger №231 (06:2x UTC):
expect = {196907: (63, 60), 196935: (16, 15), 196889: (81, 77), 196941: (1, 1), 196939: (8, 8), 196940: (4, 4), 196930: (11, 11), 191614: (7350, 7288), 196832: (224, 224), 196874: (67, 65)}
bad = []
for tid, (lpn, cc) in expect.items():
    got = state.get(str(tid), {})
    if got.get('lpn') != lpn or got.get('cc') != cc:
        bad.append((tid, got, (lpn, cc)))
print('сверка ledger №231:', f'OK все {len(expect)} точек' if not bad else f'РАСХОЖДЕНИЯ: {bad}')
