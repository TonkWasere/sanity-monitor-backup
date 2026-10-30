#!/usr/bin/env python3
# derive_175.py — генерация tools/rescan54_175_fetch.py из rescan54_174_fetch.py:
# TS 1330->1430, WIN 12:30->13:30, prev 174->175 (вход) / 175->176 (выход),
# WATCH/KNOWN/резюме +196902/+196903/+196904 (NEW 54-174), DONE 54-175, шапка «WIPE-14 восстановлен».
import ast

src = open('/home/z/my-project/tools/rescan54_174_fetch.py').read()

head_end = src.index('import json, os, urllib.request')
new_head = '''# rescan54_175_fetch.py — Task 54-175: часовой cron-раунд ~14:28 UTC 23.10 (WIPE-14: 7-Й ОТКАТ ВМ,
# серия снова активна после 4 чистых часов; вслепую восстановлен за ~2 мин: stash → fetch → ff-only
# 6151e4ff (0 потерь) → vault creds (эталон 7f9edd5d, API 200) → prev_lpn_175 реанимирован из TS1330
# снапов 78/78). Окно 1 ч: 13:30->14:30 (54-174 закрыт ~13:44). Watch-list из №214: целотредовый снос
# 196887 (cc=237, вырезы пошли — 5)?; доживёт ли твинк-личнотред 196902?; вирус 196903 датомайнинг?;
# 196834 вырезы (4)?; 196894 4-й вырез?; 196867 серверный разгон?; Crios 17+ ч; @Рупоры ~18-19 ч;
# ОТС-итоги X+3; Санити 48-й; канон 47-й; 404 83-й; Празднество 28.10; PAT №49
'''
src = new_head + src[head_end:]

edits = [
    ("TS = '20261023_1330'", "TS = '20261023_1430'"),
    ("WIN = '2026-10-23T12:30'  # окно 1 ч (54-173 закрыт ~12:44)",
     "WIN = '2026-10-23T13:30'  # окно 1 ч (54-174 закрыт ~13:44)"),
    ("vs prev_lpn_174 (база 12:30, окно 1 ч)", "vs prev_lpn_175 (база 13:30, окно 1 ч)"),
    ("prev = json.load(open('/tmp/prev_lpn_174.json'))", "prev = json.load(open('/tmp/prev_lpn_175.json'))"),
    ("(база prev_lpn_174: {len(prev)} ключей, 12:30 UTC — +196896/+196898)",
     "(база prev_lpn_175: {len(prev)} ключей, 13:30 UTC — реанимирована из TS1330-снапов после WIPE-14)"),
    ("open('/tmp/prev_lpn_175.json', 'w')", "open('/tmp/prev_lpn_176.json', 'w')"),
    (">>> prev_lpn_175.json сохранён", ">>> prev_lpn_176.json сохранён"),
    # WATCH: +196902/+196903/+196904 (NEW 54-174)
    ("196887, 196888, 196890, 196891, 196893, 196834, 196894, 196876, 196883, 196895, 196896, 196898]",
     "196887, 196888, 196890, 196891, 196893, 196834, 196894, 196876, 196883, 196895, 196896, 196898, 196902, 196903, 196904]"),
    # KNOWN: строка заканчивается }
    ("196887, 196888, 196890, 196891, 196893, 196894, 196876, 196883, 196895, 196896, 196898}",
     "196887, 196888, 196890, 196891, 196893, 196894, 196876, 196883, 196895, 196896, 196898, 196902, 196903, 196904}"),
    ("thread_summary(196898)",
     "thread_summary(196898)\nthread_summary(196902)\nthread_summary(196903)\nthread_summary(196904)"),
    ("DONE 54-174 PHASE1+2", "DONE 54-175 PHASE1+2"),
]
for old, new in edits:
    if src.count(old) != 1:
        raise SystemExit(f'FATAL: [{src.count(old)}] вхождений якоря: {old[:60]}')
    src = src.replace(old, new)

ast.parse(src)  # syntax check
open('/home/z/my-project/tools/rescan54_175_fetch.py', 'w').write(src)
print('rescan54_175_fetch.py записан, правок:', len(edits), '— syntax OK')
