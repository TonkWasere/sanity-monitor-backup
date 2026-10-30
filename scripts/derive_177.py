#!/usr/bin/env python3
# derive_177.py — генерация tools/rescan54_177_fetch.py из rescan54_176_fetch.py:
# TS 1530->1630, WIN 14:30->15:30, prev 176->177 (вход) / 177->178 (выход),
# WATCH/KNOWN/резюме +196897/+196911/+196912 (NEW 54-176), DONE 54-177, шапка «WIPE-15».
import ast

src = open('/home/z/my-project/tools/rescan54_176_fetch.py').read()

head_end = src.index('import json, os, urllib.request')
new_head = '''# rescan54_177_fetch.py — Task 54-177: часовой cron-раунд ~16:28 UTC 23.10 (WIPE-15: 8-Й ОТКАТ ВМ
# — снова после 1 чистого часа; вслепую восстановлен за ~3 мин: stash wipe15-artifacts-1628 →
# fetch → ff-only 02bdac2f (0 потерь, 54-176 уже был в remote) → vault creds (эталон 7f9edd5d,
# API 200) → prev_lpn_177 реанимирован из TS1530-снапов 83/83, sanity 17/17).
# Окно 1 ч: 15:30->16:30 (54-176 закрыт ~15:38). Watch-list из №216: волна «ТУШИЙ ПРИЗРАК»
# 196905 3-й час разгон?/снос треда?; гэп 196904 растёт?; связка ТГ-карточек: волна тредов
# о перс-магазине/скидках?; 196887 действительно конец залива?; 196834 8-й вырез?;
# Crios ~19-20 ч; @Рупоры ~20-й; Санити 50-й; GG 25-й; канон 49-й; 404 85-й;
# ОТС-итоги X+3 (~143 ч); флешмоб ~105-й; ТГК 3234; Празднество 28.10; PAT №51
'''
src = new_head + src[head_end:]

edits = [
    ("TS = '20261023_1530'", "TS = '20261023_1630'"),
    ("WIN = '2026-10-23T14:30'  # окно 1 ч (54-175 закрыт ~14:44)",
     "WIN = '2026-10-23T15:30'  # окно 1 ч (54-176 закрыт ~15:38)"),
    ("vs prev_lpn_176 (база 14:30, окно 1 ч)", "vs prev_lpn_177 (база 15:30, окно 1 ч)"),
    ("prev = json.load(open('/tmp/prev_lpn_176.json'))", "prev = json.load(open('/tmp/prev_lpn_177.json'))"),
    ("(база prev_lpn_176: {len(prev)} ключей, 14:30 UTC — +196905/+196906)",
     "(база prev_lpn_177: {len(prev)} ключей, 15:30 UTC — +196897/+196911/+196912; реанимирована после WIPE-15)"),
    ("open('/tmp/prev_lpn_177.json', 'w')", "open('/tmp/prev_lpn_178.json', 'w')"),
    (">>> prev_lpn_177.json сохранён", ">>> prev_lpn_178.json сохранён"),
    # WATCH: +196897/+196911/+196912 (NEW 54-176)
    ("196902, 196903, 196904, 196905, 196906]",
     "196902, 196903, 196904, 196905, 196906, 196897, 196911, 196912]"),
    # KNOWN: строка заканчивается }
    ("196902, 196903, 196904, 196905, 196906}",
     "196902, 196903, 196904, 196905, 196906, 196897, 196911, 196912}"),
    ("thread_summary(196906)",
     "thread_summary(196906)\nthread_summary(196897)\nthread_summary(196911)\nthread_summary(196912)"),
    ("DONE 54-176 PHASE1+2", "DONE 54-177 PHASE1+2"),
]
for old, new in edits:
    if src.count(old) != 1:
        raise SystemExit(f'FATAL: [{src.count(old)}] вхождений якоря: {old[:60]}')
    src = src.replace(old, new)

ast.parse(src)  # syntax check
open('/home/z/my-project/tools/rescan54_177_fetch.py', 'w').write(src)
print('rescan54_177_fetch.py записан, правок:', len(edits), '— syntax OK')
