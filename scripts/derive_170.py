#!/usr/bin/env python3
# derive_170.py — генерация tools/rescan54_170_fetch.py из rescan54_169_fetch.py (12 правок):
# TS 0830->0930, WIN 07:30->08:30, prev 169->170 (вход) / 170->171 (выход),
# WATCH +196887/196888/196890/196891, KNOWN +196834/196887/196888/196890/196891,
# резюме +196887/196888/196890/196891, DONE 54-170, шапка WIPE-13.
src = open('/home/z/my-project/tools/rescan54_169_fetch.py').read()

head_end = src.index('import json, os, urllib.request')
new_head = '''# rescan54_170_fetch.py — Task 54-170: часовой cron-раунд ~09:28 UTC 23.10 после WIPE-13
# (6-Й ОТКАТ: диск снова 71c70b83 19.10 23:43; ff-only до a878ad73 0 потерь, vault 7f9edd5d=эталон,
# creds API 200, prev_lpn_170 реанимирован из TS0830-снапов 68/68). Раунд 54-169 выполнил
# параллельный loop 08:28-08:37 (ledger 209, NEW x3: 196888/196890/196891).
# Окно 1 ч: 08:30->09:30. Watch-list из №209: 196887 (73/75, 2 выреза держатся, ТРЕТИЙ твин
# 76561198978348618 фLOODит) - кандидат на целотредовый снос; 196832 200+?; Колизей-волна
# исчерпана (196875/196872/196877/196879 все 0) - реанимируется?; Crios 12+ ч молчит;
# 196867 @Рупоры ~13-14 ч игнор; полупризрак 196852; Санити 44-Й ЧАС; ТГК 3227 18-Й ЧАС (рекорд);
# канон 43-Й; ОТС-итоги (день X+3); 404 79-Й; PAT-напоминание №44
'''
src = new_head + src[head_end:]

edits = [
    ("TS = '20261023_0830'", "TS = '20261023_0930'"),
    ("WIN = '2026-10-23T07:30'  # окно 1 ч (54-168 закрыт 07:52)",
     "WIN = '2026-10-23T08:30'  # окно 1 ч (54-169 закрыт 08:37)"),
    ("vs prev_lpn_169 (база 07:30, окно 1 ч)", "vs prev_lpn_170 (база 08:30, окно 1 ч)"),
    ("prev = json.load(open('/tmp/prev_lpn_169.json'))", "prev = json.load(open('/tmp/prev_lpn_170.json'))"),
    ("(база prev_lpn_169: {len(prev)} ключей, 07:30 UTC — реанимирована из TS0730-снапов после WIPE-12)",
     "(база prev_lpn_170: {len(prev)} ключей, 08:30 UTC — реанимирована из TS0830-снапов после WIPE-13)"),
    ("open('/tmp/prev_lpn_170.json', 'w')", "open('/tmp/prev_lpn_171.json', 'w')"),
    (">>> prev_lpn_170.json сохранён", ">>> prev_lpn_171.json сохранён"),
    # WATCH: добавить новыс 54-169 (строка заканчивается ])
    ("196879, 193924, 196852]",
     "196879, 193924, 196852, 196887, 196888, 196890, 196891]"),
    # KNOWN: строка заканчивается }
    ("196879, 193924, 196852}",
     "196879, 193924, 196852, 196834, 196887, 196888, 196890, 196891}"),
    ("thread_summary(193924)",
     "thread_summary(193924)\nthread_summary(196887)\nthread_summary(196888)\nthread_summary(196890)\nthread_summary(196891)"),
    ("DONE 54-169 PHASE1+2", "DONE 54-170 PHASE1+2"),
]
for old, new in edits:
    if src.count(old) != 1:
        raise SystemExit(f'FATAL: [{src.count(old)}] вхождений якоря: {old[:60]}')
    src = src.replace(old, new)

open('/home/z/my-project/tools/rescan54_170_fetch.py', 'w').write(src)
print('rescan54_170_fetch.py записан, правок:', len(edits))
