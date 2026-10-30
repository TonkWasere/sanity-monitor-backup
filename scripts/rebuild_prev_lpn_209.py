#!/usr/bin/env python3
# rebuild_prev_lpn_209.py — /tmp-чистка между раундами (НЕ вайп ВМ: git-стейт и
# young-state целы, healthcheck 12/12 00:21 UTC): восстановление /tmp/prev_lpn_209.json
# из git-снапов near999999 20261024_2320 (база 54-208, 23:20-23:39 UTC, HEAD 260d1241)
# + lite-надстройка 00:10 SNAP15 (196982 2/2, 196983 2/2, 196984 1/1 — дельты
# после закрытия 54-208). Эталон: ledger №248 (151 кл, +1 NEW 196982).
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_2320.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_2320\.json', os.path.basename(fn))
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

print(f'>>> база TS2320: {len(cur)} ключей')

# Контроль базы TS2320 против эталона №248 (значения на 23:2x)
checks_ts = {
    196982: (1, 1),      # NEW 23:26:47 «Корея - Итоги», первый замер
    196949: (50, 50),    # +7 разгон (43→50)
    196939: (27, 26),    # «Сборояка на кровоток» +2, гэп 1
    196973: (25, 25),    # худший игрок +2
    196975: (24, 24),    # арбитр ожил +2
    196972: (37, 37),    # stm-баланс замер
    196974: (13, 13),    # фидбек арены замер
    196976: (7, 7),      # «Халява прийдёт» замер
    196977: (2, 2),      # «Stalzone удаляет акк» замер
    196979: (2, 2),      # «калибровка» замер
    196907: (106, 102),  # +1, гэп 4
    196966: (23, 21),    # +1, гэп 2
    196943: (183, 181),  # замер
    196956: (16, 15),    # вырез-подозрение, гэп 1
    196902: (69, 69),    # замер
    196834: (64, 57),    # гэп 7
    196875: (81, 81),    # колизей
    196927: (36, 36),    # замер
    196424: (165, 160),  # ОТС тихая линия
    196425: (132, 125),  # ОТС сбор
    196480: (172, 171),  # компенсация
    196411: (90, 85),    # мета-тред заморожен 46-й час
    191614: (7379, 7315),  # кот-тред
    196899: (9, 9),      # замер
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
print(f'>>> контроль базы TS2320: {ok}/{len(checks_ts)} совпали, miss={miss}')

# Верификация lite-надстройки по снапам SNAP15 00:10 (свидетельство lite-прогона)
for tid, want in [(196982, (2, 2)), (196983, (2, 2)), (196984, (1, 1))]:
    fn = os.path.join(OUT, f'discussion_{tid}_near999999_SNAP15_20261025_0010.json')
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {})
        got = (aa.get('lastPostNumber'), aa.get('commentCount'))
        print(f'  lite-снап {tid}: lpn/cc {got[0]}/{got[1]} (ожидалось {want[0]}/{want[1]})', 'OK' if got == want else 'RASXOZDENIE')
    except Exception as e:
        print(f'  lite-снап {tid}: нет/ошибка ({e}) — беру значение из lite-строки 00:10 worklog')

# Lite-надстройка (SNAP15 00:10 — новее базы 23:2x; события 54-0-s15 в worklog)
lite = {
    196982: {'lpn': 2, 'cc': 2},  # «Корея - Итоги» 1→2 (первый ответ, 00:10)
    196983: {'lpn': 2, 'cc': 2},  # «Высеры» NEW 23:47:12, 1→2 (00:10)
    196984: {'lpn': 1, 'cc': 1},  # «Кибербезопастность U2F» NEW 00:05:55 (1/1)
}
for tid, v in lite.items():
    old = cur.get(tid)
    cur[tid] = v
    print(f'  lite-надстройка {tid}: {old} → {v}')
json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_209.json', 'w'))
print(f'>>> prev_lpn_209.json восстановлен: {len(cur)} ключей (lite-надстройка ×{len(lite)})')
