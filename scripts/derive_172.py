#!/usr/bin/env python3
# derive_172.py — генерация tools/rescan54_172_fetch.py из rescan54_171_fetch.py:
# TS 1030->1130, WIN 09:30->10:30, prev 171->172 (вход) / 172->173 (выход),
# WATCH/KNOWN/резюме +196894 (офиц. анонс) +196876/+196883 (ложные NEW в базлайне),
# DONE 54-172, шапка «второй час без WIPE».
import ast

src = open('/home/z/my-project/tools/rescan54_171_fetch.py').read()

head_end = src.index('import json, os, urllib.request')
new_head = '''# rescan54_172_fetch.py — Task 54-172: часовой cron-раунд ~11:28 UTC 23.10 (второй час подряд БЕЗ WIPE:
# healthcheck 11:29 = 12/12, HEAD 037dcc26 = origin = backup, prev_lpn_172 цел 72 ключа; 54-171 выполнен
# параллельным loop'ом). Окно 1 ч: 10:30->11:30 (54-171 закрыт ~10:41). Watch-list из №211: целотредовый
# снос 196887 (cc=125, 4-й час залива, оба выреза)?; темп вырезов в офиц. 196894 (2 выреза за 1-й час —
# повторит ритм 196411?); 196893 футаж КВ вирус 3-й час?; 196832 после взятия 200 (207); Колизей 196874
# (1 вырез); Crios 14+ ч молчит; @Рупоры ~15-16 ч; ОТС-итоги X+3; Санити 45-й; канон 44-й; 404 80-й;
# Празднество-ивент 28.10; PAT №46
'''
src = new_head + src[head_end:]

edits = [
    ("TS = '20261023_1030'", "TS = '20261023_1130'"),
    ("WIN = '2026-10-23T09:30'  # окно 1 ч (54-170 закрыт 09:46)",
     "WIN = '2026-10-23T10:30'  # окно 1 ч (54-171 закрыт ~10:41)"),
    ("vs prev_lpn_171 (база 09:30, окно 1 ч)", "vs prev_lpn_172 (база 10:30, окно 1 ч)"),
    ("prev = json.load(open('/tmp/prev_lpn_171.json'))", "prev = json.load(open('/tmp/prev_lpn_172.json'))"),
    ("(база prev_lpn_171: {len(prev)} ключей, 09:30 UTC — +196893, 196834 добан отдельным GET)",
     "(база prev_lpn_172: {len(prev)} ключей, 10:30 UTC — +196894/+196876/+196883)"),
    ("open('/tmp/prev_lpn_172.json', 'w')", "open('/tmp/prev_lpn_173.json', 'w')"),
    (">>> prev_lpn_172.json сохранён", ">>> prev_lpn_173.json сохранён"),
    # WATCH: +196894 (офиц. анонс Празднества) + 196876/196883 (ложные NEW, добраны в базлайн 54-171)
    ("196887, 196888, 196890, 196891, 196893, 196834]",
     "196887, 196888, 196890, 196891, 196893, 196834, 196894, 196876, 196883]"),
    # KNOWN: строка заканчивается }
    ("196887, 196888, 196890, 196891, 196893}",
     "196887, 196888, 196890, 196891, 196893, 196894, 196876, 196883}"),
    ("thread_summary(196893)",
     "thread_summary(196893)\nthread_summary(196894)\nthread_summary(196876)\nthread_summary(196883)"),
    ("DONE 54-171 PHASE1+2", "DONE 54-172 PHASE1+2"),
]
for old, new in edits:
    if src.count(old) != 1:
        raise SystemExit(f'FATAL: [{src.count(old)}] вхождений якоря: {old[:60]}')
    src = src.replace(old, new)

ast.parse(src)  # syntax check
open('/home/z/my-project/tools/rescan54_172_fetch.py', 'w').write(src)
print('rescan54_172_fetch.py записан, правок:', len(edits), '— syntax OK')
