#!/usr/bin/env python3
# rebuild_prev_lpn_198.py — WIPE-27: восстановление /tmp/prev_lpn_198.json
# из git-снапов near999999 20261024_1220 (база 54-197, 12:21-12:39 UTC).
# Эталон: ledger №237 «PREV_LPN: /tmp/prev_lpn_198.json 132 ключей».
# ВАЖНО: 196960 в снапах 1220 ОТСУТСТВУЕТ (рождён 12:29 после закрытия окна) —
# в 54-198 будет «ЛИН/НЕТ В PREV», это штатно.
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
cur = {}
for fn in glob.glob(os.path.join(OUT, 'discussion_*_near999999_20261024_1220.json')):
    m = re.match(r'discussion_(\d+)_near999999_20261024_1220\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        cur[int(m.group(1))] = {'lpn': aa.get('lastPostNumber'), 'cc': aa.get('commentCount')}
    except Exception as e:
        print(f'  parse fail {fn}: {e}')

json.dump({str(k): v for k, v in cur.items()}, open('/tmp/prev_lpn_198.json', 'w'))
print(f'>>> prev_lpn_198.json восстановлен: {len(cur)} ключей (эталон №237: 132)')

# Контрольные точки против ledger №237 (значения на 12:2x-12:3x)
checks = {
    196943: (123, 121),  # «Рейтинг празднества» 5-я волна +22
    196959: (13, 11),    # NEW ливер-rage (2 выреза на старте)
    196952: (27, 27),    # «Баланс с отс» stm-OP young-взрыв
    196953: (14, 14),    # «IWI Tavor»
    196956: (6, 6),      # «Встречайте исправление багов форума!» stm
    196955: (8, 8),      # «Празднаство»
    196954: (13, 13),    # «Так алё я не понял» stm-OP
    196950: (3, 3),      # «Проблема с отс» мёртв
    196951: (13, 13),    # young
    196902: (43, 43),    # «Замок Сефиры» вспышка +12, Crios ×2
    196946: (30, 30),    # «распреду» 5-й час
    196949: (28, 28),    # «нерфят арт» graduated жив
    196907: (80, 76),    # ОТС-фидбек пауза
    196889: (85, 81),    # клиент-реквесты пауза
    196778: (60, 58),    # Цепь Распада
    131836: (193, 186),  # офиц. тред распределения
    196411: (90, 85),    # мета-тред заморожен 35 ч+
    196424: (165, 160),  # ОТС ~164 ч
    196452: (30, 30),    # флешмоб талонов 126-й
    191614: (7354, 7291),  # кот-тред
    112917: (67773, 66520),  # мегатред вайб
    196480: (172, 171),  # компенсация
    196488: (48, 45),    # кейс
    196425: (131, 124),  # сбор ОТС
}
ok = miss = 0
for tid, (lpn, cc) in checks.items():
    v = cur.get(tid)
    if not v:
        print(f'  MISS {tid}'); miss += 1; continue
    good = v['lpn'] == lpn and v['cc'] == cc
    ok += good
    if not good:
        print(f'  MISMATCH {tid}: {v} ожидалось lpn={lpn} cc={cc}')
print(f'контроль: {ok}/{len(checks)} OK, miss={miss}')
print(f'196960 в базе: {"ДА (неожиданно)" if 196960 in cur else "нет — штатно (рождён 12:29 после окна 1220)"}')
