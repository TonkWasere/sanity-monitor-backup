#!/usr/bin/env python3
# derive_174.py — генерация tools/rescan54_174_fetch.py из rescan54_173_fetch.py:
# TS 1230->1330, WIN 11:30->12:30, prev 173->174 (вход) / 174->175 (выход),
# WATCH/KNOWN/резюме +196896/+196898 (NEW 54-173), DONE 54-174, шапка «четвёртый час без WIPE».
import ast

src = open('/home/z/my-project/tools/rescan54_173_fetch.py').read()

head_end = src.index('import json, os, urllib.request')
new_head = '''# rescan54_174_fetch.py — Task 54-174: часовой cron-раунд ~13:28 UTC 23.10 (ЧЕТВЁРТЫЙ час подряд БЕЗ WIPE:
# healthcheck 13:28 = 12/12, HEAD bc2167f2 = origin = backup, prev_lpn_174 цел 75 ключей). Окно 1 ч:
# 12:30->13:30 (54-173 закрыт ~12:44). Watch-list из №213: целотредовый снос 196887 (cc=213, ~250 постов
# за 6 ч)?; догонит ли 196894 ритм 196411 (3-й вырез вернулся)?; первые вырезы в 196896/196898?;
# 196893 вирус 4-й час?; 196867 после оживления?; 196874 2-й вырез; Crios 16+ ч; @Рупоры ~17-18 ч;
# ОТС-итоги X+3; Санити 47-й; канон 46-й; 404 82-й; Празднество 28.10; PAT №48
'''
src = new_head + src[head_end:]

edits = [
    ("TS = '20261023_1230'", "TS = '20261023_1330'"),
    ("WIN = '2026-10-23T11:30'  # окно 1 ч (54-172 закрыт ~11:36)",
     "WIN = '2026-10-23T12:30'  # окно 1 ч (54-173 закрыт ~12:44)"),
    ("vs prev_lpn_173 (база 11:30, окно 1 ч)", "vs prev_lpn_174 (база 12:30, окно 1 ч)"),
    ("prev = json.load(open('/tmp/prev_lpn_173.json'))", "prev = json.load(open('/tmp/prev_lpn_174.json'))"),
    ("(база prev_lpn_173: {len(prev)} ключей, 11:30 UTC — +196895)",
     "(база prev_lpn_174: {len(prev)} ключей, 12:30 UTC — +196896/+196898)"),
    ("open('/tmp/prev_lpn_174.json', 'w')", "open('/tmp/prev_lpn_175.json', 'w')"),
    (">>> prev_lpn_174.json сохранён", ">>> prev_lpn_175.json сохранён"),
    # WATCH: +196896/+196898 (NEW 54-173)
    ("196887, 196888, 196890, 196891, 196893, 196834, 196894, 196876, 196883, 196895]",
     "196887, 196888, 196890, 196891, 196893, 196834, 196894, 196876, 196883, 196895, 196896, 196898]"),
    # KNOWN: строка заканчивается }
    ("196887, 196888, 196890, 196891, 196893, 196894, 196876, 196883, 196895}",
     "196887, 196888, 196890, 196891, 196893, 196894, 196876, 196883, 196895, 196896, 196898}"),
    ("thread_summary(196895)",
     "thread_summary(196895)\nthread_summary(196896)\nthread_summary(196898)"),
    ("DONE 54-173 PHASE1+2", "DONE 54-174 PHASE1+2"),
]
for old, new in edits:
    if src.count(old) != 1:
        raise SystemExit(f'FATAL: [{src.count(old)}] вхождений якоря: {old[:60]}')
    src = src.replace(old, new)

ast.parse(src)  # syntax check
open('/home/z/my-project/tools/rescan54_174_fetch.py', 'w').write(src)
print('rescan54_174_fetch.py записан, правок:', len(edits), '— syntax OK')
