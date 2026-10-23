#!/usr/bin/env python3
# derive_171.py — генерация tools/rescan54_171_fetch.py из rescan54_170_fetch.py:
# TS 0930->1030, WIN 08:30->09:30, prev 170->171 (вход) / 171->172 (выход),
# WATCH +196893/+196834 (вернул), KNOWN +196893, резюме +196893, DONE 54-171, шапка «без WIPE».
src = open('/home/z/my-project/tools/rescan54_170_fetch.py').read()

head_end = src.index('import json, os, urllib.request')
new_head = '''# rescan54_171_fetch.py — Task 54-171: часовой cron-раунд ~10:28 UTC 23.10 (ВПЕРВЫЕ ЗА 3 Ч БЕЗ WIPE:
# диск пережил час, healthcheck 10:28 = 12/12, HEAD 5bc5da7f = origin = backup, prev_lpn_171 цел).
# Окно 1 ч: 09:30->10:30 (54-170 закрыт 09:46). Watch-list из №210: снесут ли 196887 (cc=98, 3-й час
# залива, 2 выреза)?; 196893 «Потерянный футаж с КВ» вирусный?; 196822 удвоение продолжится?;
# Колизей-волна в соседях (196874 +4); 196832 200+? (замедление +80/+6/+3); Crios 13+ ч молчит;
# @Рупоры ~14-15 ч; ТГК 3227 18-Й ЧАС (РЕКОРД); ОТС-итоги X+3; Санити 44-й; канон 43-й; 404 79-й;
# PAT №45; 196834 вернул в WATCH (урок №210 — выпадал из базлайна)
'''
src = new_head + src[head_end:]

edits = [
    ("TS = '20261023_0930'", "TS = '20261023_1030'"),
    ("WIN = '2026-10-23T08:30'  # окно 1 ч (54-169 закрыт 08:37)",
     "WIN = '2026-10-23T09:30'  # окно 1 ч (54-170 закрыт 09:46)"),
    ("vs prev_lpn_170 (база 08:30, окно 1 ч)", "vs prev_lpn_171 (база 09:30, окно 1 ч)"),
    ("prev = json.load(open('/tmp/prev_lpn_170.json'))", "prev = json.load(open('/tmp/prev_lpn_171.json'))"),
    ("(база prev_lpn_170: {len(prev)} ключей, 08:30 UTC — реанимирована из TS0830-снапов после WIPE-13)",
     "(база prev_lpn_171: {len(prev)} ключей, 09:30 UTC — +196893, 196834 добан отдельным GET)"),
    ("open('/tmp/prev_lpn_171.json', 'w')", "open('/tmp/prev_lpn_172.json', 'w')"),
    (">>> prev_lpn_171.json сохранён", ">>> prev_lpn_172.json сохранён"),
    # WATCH: добавить 196893 (новый) + 196834 (вернуть) — строка заканчивается ]
    ("196887, 196888, 196890, 196891]",
     "196887, 196888, 196890, 196891, 196893, 196834]"),
    # KNOWN: строка заканчивается }
    ("196887, 196888, 196890, 196891}",
     "196887, 196888, 196890, 196891, 196893}"),
    ("thread_summary(196891)",
     "thread_summary(196891)\nthread_summary(196893)"),
    ("DONE 54-170 PHASE1+2", "DONE 54-171 PHASE1+2"),
]
for old, new in edits:
    if src.count(old) != 1:
        raise SystemExit(f'FATAL: [{src.count(old)}] вхождений якоря: {old[:60]}')
    src = src.replace(old, new)

open('/home/z/my-project/tools/rescan54_171_fetch.py', 'w').write(src)
print('rescan54_171_fetch.py записан, правок:', len(edits))
