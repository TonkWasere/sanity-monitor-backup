#!/usr/bin/env python3
# derive_173.py — генерация tools/rescan54_173_fetch.py из rescan54_172_fetch.py:
# TS 1130->1230, WIN 10:30->11:30, prev 172->173 (вход) / 173->174 (выход),
# WATCH/KNOWN/резюме +196895 (privileges-протест), DONE 54-173, шапка «третий час без WIPE».
import ast

src = open('/home/z/my-project/tools/rescan54_172_fetch.py').read()

head_end = src.index('import json, os, urllib.request')
new_head = '''# rescan54_173_fetch.py — Task 54-173: часовой cron-раунд ~12:28 UTC 23.10 (ТРЕТИЙ час подряд БЕЗ WIPE:
# healthcheck 12:28 = 12/12, HEAD 1ed61625 = origin = backup, prev_lpn_173 цел 73 ключа). Окно 1 ч:
# 11:30->12:30 (54-172 закрыт ~11:36). Watch-list из №212: снесут ли наконец 196887 (cc=173, темп ×2,
# 5-й час залива)?; 196895 privileges-протест — эхо «грехов»?; вернутся ли вырезы в 196894 (2 status quo)?;
# 196876 всплеск после +13?; 196834 разгон 4-й час?; 196874 2-й вырез; Crios 15+ ч; @Рупоры ~16-17 ч;
# ОТС-итоги X+3; Санити 46-й; канон 45-й; 404 81-й; Празднество 28.10; PAT №47
'''
src = new_head + src[head_end:]

edits = [
    ("TS = '20261023_1130'", "TS = '20261023_1230'"),
    ("WIN = '2026-10-23T10:30'  # окно 1 ч (54-171 закрыт ~10:41)",
     "WIN = '2026-10-23T11:30'  # окно 1 ч (54-172 закрыт ~11:36)"),
    ("vs prev_lpn_172 (база 10:30, окно 1 ч)", "vs prev_lpn_173 (база 11:30, окно 1 ч)"),
    ("prev = json.load(open('/tmp/prev_lpn_172.json'))", "prev = json.load(open('/tmp/prev_lpn_173.json'))"),
    ("(база prev_lpn_172: {len(prev)} ключей, 10:30 UTC — +196894/+196876/+196883)",
     "(база prev_lpn_173: {len(prev)} ключей, 11:30 UTC — +196895)"),
    ("open('/tmp/prev_lpn_173.json', 'w')", "open('/tmp/prev_lpn_174.json', 'w')"),
    (">>> prev_lpn_173.json сохранён", ">>> prev_lpn_174.json сохранён"),
    # WATCH: +196895 (privileges-протест, NEW 54-172)
    ("196887, 196888, 196890, 196891, 196893, 196834, 196894, 196876, 196883]",
     "196887, 196888, 196890, 196891, 196893, 196834, 196894, 196876, 196883, 196895]"),
    # KNOWN: строка заканчивается }
    ("196887, 196888, 196890, 196891, 196893, 196894, 196876, 196883}",
     "196887, 196888, 196890, 196891, 196893, 196894, 196876, 196883, 196895}"),
    ("thread_summary(196883)",
     "thread_summary(196883)\nthread_summary(196895)"),
    ("DONE 54-172 PHASE1+2", "DONE 54-173 PHASE1+2"),
]
for old, new in edits:
    if src.count(old) != 1:
        raise SystemExit(f'FATAL: [{src.count(old)}] вхождений якоря: {old[:60]}')
    src = src.replace(old, new)

ast.parse(src)  # syntax check
open('/home/z/my-project/tools/rescan54_173_fetch.py', 'w').write(src)
print('rescan54_173_fetch.py записан, правок:', len(edits), '— syntax OK')
