#!/usr/bin/env python3
# rebuild_prev_lpn_210.py — WIPE-28 (28-й откат ВМ, окно 00:30-00:55 UTC 25.10,
# пойман интерраундом 54-209-B): /tmp/prev_lpn_209/_210 снесены вместе с creds.
# Восстановление /tmp/prev_lpn_210.json из git-снапов near999999 20261025_0020
# (база 54-209, 00:20-00:4x UTC, HEAD 11258f0e). Эталон: ledger №249.
# (54-209-B к этому моменту уже восстановил creds+reset --hard → снапы 0020 на диске.)
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261025_0020.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261025_0020\.json', os.path.basename(fn))
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

print(f'>>> база TS0020: {len(cur)} ключей')

# Контроль базы TS0020 против эталона №249 (значения на 00:2x)
checks_ts = {
    196984: (4, 3),      # ★ ВЫРЕЗ на молодом: LPN 1→4, cc 1→3, гэп 1 (№249)
    196976: (9, 9),      # young-разгон +2 (7→9/9)
    196977: (3, 3),      # young-разгон +1 (2→3/3)
    196949: (50, 50),    # замер (разгон кончился)
    196939: (27, 26),    # замер, гэп 1
    196973: (26, 26),    # +1
    196975: (25, 25),    # арбитр +1
    196972: (37, 37),    # stm-баланс
    196979: (2, 2),      # young замер
    196982: (2, 2),      # young замер
    196983: (2, 2),      # young замер
    196907: (106, 102),  # гэп 4
    196966: (23, 21),    # гэп 2
    196943: (183, 181),  # замер
    196956: (16, 15),    # вырез-подозрение, гэп 1
    196902: (69, 69),    # замер
    196834: (64, 57),    # гэп 7
    196875: (81, 81),    # колизей
    196927: (36, 36),    # замер
    196424: (165, 160),  # ОТС тихая линия
    196425: (132, 125),  # ОТС сбор
    196480: (172, 171),  # компенсация
    196411: (90, 85),    # мета-тред заморожен 47-й час
    191614: (7379, 7315),  # кот-тред
    196488: (48, 45),    # кейс
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
print(f'>>> контроль базы TS0020: {ok}/{len(checks_ts)} совпали, miss={miss}')

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_210.json', 'w'))
print(f'>>> prev_lpn_210.json восстановлен: {len(cur)} ключей')
