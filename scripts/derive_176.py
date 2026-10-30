#!/usr/bin/env python3
# derive_176.py — генерация tools/rescan54_176_fetch.py из rescan54_175_fetch.py:
# TS 1430->1530, WIN 13:30->14:30, prev 175->176 (вход) / 176->177 (выход),
# WATCH/KNOWN/резюме +196905/+196906 (NEW 54-175), DONE 54-176, шапка «аудит вырезов».
import ast

src = open('/home/z/my-project/tools/rescan54_175_fetch.py').read()

head_end = src.index('import json, os, urllib.request')
new_head = '''# rescan54_176_fetch.py — Task 54-176: часовой cron-раунд ~15:28 UTC 23.10 (5-й час подряд
# БЕЗ WIPE; HEAD 5029191c = origin = backup; по пути сделан аудит вырезов по запросу автора:
# 611 поймано / 608 с текстом в гите, таблица CUTS_TABLE_20261023.md — 191614=164, 196501=74,
# 196799=68; 153 автора под ножом, 53 stm-твинка = 223 поста = 37%, Crios ×13).
# Окно 1 ч: 14:30->15:30 (54-175 закрыт ~14:44). Watch-list из №215: целотредовый снос 196887
# (cc=239, темп +2/ч — выдыхается)?; вирус 196903 датомайнинг (18)?; волна «ТУШИЙ ПРИЗРАК»
# 196905 (13)?; 196834 вырезы (7)?; 196894 4-й вырез?; судьба твинк-личнотреда 196902?;
# 196874 3-й вырез?; Crios 18+ ч; @Рупоры ~20-й; ОТС-итоги X+3; Санити 49-й; флешмоб ~104-й;
# канон 48-й; 404 84-й; ТГК 3227 пауза 4.5 ч; Празднество 28.10; PAT №50
'''
src = new_head + src[head_end:]

edits = [
    ("TS = '20261023_1430'", "TS = '20261023_1530'"),
    ("WIN = '2026-10-23T13:30'  # окно 1 ч (54-174 закрыт ~13:44)",
     "WIN = '2026-10-23T14:30'  # окно 1 ч (54-175 закрыт ~14:44)"),
    ("vs prev_lpn_175 (база 13:30, окно 1 ч)", "vs prev_lpn_176 (база 14:30, окно 1 ч)"),
    ("prev = json.load(open('/tmp/prev_lpn_175.json'))", "prev = json.load(open('/tmp/prev_lpn_176.json'))"),
    ("(база prev_lpn_175: {len(prev)} ключей, 13:30 UTC — реанимирована из TS1330-снапов после WIPE-14)",
     "(база prev_lpn_176: {len(prev)} ключей, 14:30 UTC — +196905/+196906)"),
    ("open('/tmp/prev_lpn_176.json', 'w')", "open('/tmp/prev_lpn_177.json', 'w')"),
    (">>> prev_lpn_176.json сохранён", ">>> prev_lpn_177.json сохранён"),
    # WATCH: +196905/+196906 (NEW 54-175)
    ("196895, 196896, 196898, 196902, 196903, 196904]",
     "196895, 196896, 196898, 196902, 196903, 196904, 196905, 196906]"),
    # KNOWN: строка заканчивается }
    ("196895, 196896, 196898, 196902, 196903, 196904}",
     "196895, 196896, 196898, 196902, 196903, 196904, 196905, 196906}"),
    ("thread_summary(196904)",
     "thread_summary(196904)\nthread_summary(196905)\nthread_summary(196906)"),
    ("DONE 54-175 PHASE1+2", "DONE 54-176 PHASE1+2"),
]
for old, new in edits:
    if src.count(old) != 1:
        raise SystemExit(f'FATAL: [{src.count(old)}] вхождений якоря: {old[:60]}')
    src = src.replace(old, new)

ast.parse(src)  # syntax check
open('/home/z/my-project/tools/rescan54_176_fetch.py', 'w').write(src)
print('rescan54_176_fetch.py записан, правок:', len(edits), '— syntax OK')
