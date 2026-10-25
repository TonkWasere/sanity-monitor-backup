#!/usr/bin/env python3
# rebuild_prev_lpn_211.py — WIPE-29 (29-й откат ВМ, окно ~01:40-01:55 UTC 25.10,
# пойман SNAP15 01:55 lite): /tmp/prev_lpn_210/_211 снесены вместе с creds+bundle.
# Восстановление /tmp/prev_lpn_211.json из git-снапов near999999 20261025_0120
# (база 54-210, обход TS0120, HEAD 45da8d9c). Эталон: ledger №250.
# (credentials уже восстановлены из MEGA vault → reset --hard вернул снапы 0120.)
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261025_0120.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261025_0120\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        lpn, cc = aa.get('lastPostNumber'), aa.get('commentCount')
        if lpn is None:
            continue
        cur[int(m.group(1))] = {'lpn': lpn, 'cc': cc}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

print(f'>>> база TS0120: {len(cur)} ключей')

# Контроль базы TS0120 против эталона №250 (значения на 01:2x, после 54-210)
checks_ts = {
    196949: (53, 53),    # ★ resumed +3 в 54-210 (50→53)
    196875: (82, 82),    # ★ колизей +1
    196982: (3, 3),      # young +1 (2→3)
    196984: (6, 5),      # ★ U2F гэп 1 удержан (4/3→6/5)
    196979: (2, 2),      # young замер
    196983: (2, 2),      # young замер
    196946: (54, 54),    # +1 в 54-210 (53→54)
    196973: (27, 27),    # +1 (26→27)
    196976: (10, 10),    # +1 (9→10), вырезов нет
    196907: (106, 102),  # гэп 4
    196956: (16, 15),    # вырез-подозрение, гэп 1
    196834: (64, 57),    # гэп 7
    196424: (165, 160),  # ОТС тихая линия
    196425: (132, 125),  # ОТС сбор
    196411: (90, 85),    # мета-тред канон #48, 84h MATCH
    191614: (7379, 7315),  # кот-тред
}
ok = miss = 0
for tid, (lpn, cc) in checks_ts.items():
    v = cur.get(tid)
    if not v:
        print(f'  MISS {tid}'); miss += 1; continue
    good = v['lpn'] == lpn and v['cc'] == cc
    ok += good
    if not good:
        print(f'  MISMATCH {tid}: {v} ожидалось lpn={lpn} cc={cc}')
print(f'>>> контроль базы TS0120: {ok}/{len(checks_ts)} совпали, miss={miss}')

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_211.json', 'w'))
print(f'>>> prev_lpn_211.json восстановлен: {len(cur)} ключей')
