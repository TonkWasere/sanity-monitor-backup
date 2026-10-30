# derive_178.py — генерация tools/rescan54_178_fetch.py из rescan54_177_fetch.py
# 11 правок: шапка (раунд 178, окно 16:30->17:30, без WIPE 6-й час, watch №217, PAT №52),
# TS 1630->1730, WIN 15:30->16:30, prev_178 load, prev_179 save, WATCH +196889/+196909/+196913/+196914,
# KNOWN +4, thread_summary +4, LPN-заголовок/база, DONE 54-178
import ast

SRC = '/home/z/my-project/tools/rescan54_177_fetch.py'
DST = '/home/z/my-project/tools/rescan54_178_fetch.py'

src = open(SRC, encoding='utf-8').read()

edits = [
    # 1) шапка
    ("# rescan54_177_fetch.py — Task 54-177: часовой cron-раунд ~16:28 UTC 23.10 (WIPE-15: 8-Й ОТКАТ ВМ\n"
     "# — снова после 1 чистого часа; вслепую восстановлен за ~3 мин: stash wipe15-artifacts-1628 →\n"
     "# fetch → ff-only 02bdac2f (0 потерь, 54-176 уже был в remote) → vault creds (эталон 7f9edd5d,\n"
     "# API 200) → prev_lpn_177 реанимирован из TS1530-снапов 83/83, sanity 17/17).\n"
     "# Окно 1 ч: 15:30->16:30 (54-176 закрыт ~15:38). Watch-list из №216: волна «ТУШИЙ ПРИЗРАК»\n"
     "# 196905 3-й час разгон?/снос треда?; гэп 196904 растёт?; связка ТГ-карточек: волна тредов\n"
     "# о перс-магазине/скидках?; 196887 действительно конец залива?; 196834 8-й вырез?;\n"
     "# Crios ~19-20 ч; @Рупоры ~20-й; Санити 50-й; GG 25-й; канон 49-й; 404 85-й;\n"
     "# ОТС-итоги X+3 (~143 ч); флешмоб ~105-й; ТГК 3234; Празднество 28.10; PAT №51",
     "# rescan54_178_fetch.py — Task 54-178: часовой cron-раунд ~17:28 UTC 23.10 (БЕЗ WIPE —\n"
     "# 6-й чистый час подряд; HEAD 70cbbe20 = origin = backup; healthcheck 12/12 ЗДОРОВ).\n"
     "# Окно 1 ч: 16:30->17:30 (54-177 закрыт ~16:3x; WIPE-15 вслепую закрыт за ~3 мин).\n"
     "# Watch-list из №217: 196911 перс-магазин 3-й час взрыва (+29/+28 во 2-м, 51/50)?;\n"
     "# 196905 ретро-скрытие #23 — продолжение задних резок?; 196889 ОТС «Празднество» гэп-3\n"
     "# растёт?; 196834 8-й вырез?; 196887 залив +1 не мёртв — растёт?; 196897 судьба\n"
     "# (1 вырез)?; 196902 ожил — растёт?; Crios ~21 ч; @Рупоры ~21-й; Санити 51-й; GG 26-й;\n"
     "# канон 50-й; 404 86-й; ОТС-итоги X+3 (~144 ч); флешмоб ~106-й; ТГК 3235;\n"
     "# спектрум 24+ ч; PAT №52"),
    # 2) TS
    ("TS = '20261023_1630'", "TS = '20261023_1730'"),
    # 3) WIN
    ("WIN = '2026-10-23T15:30'  # окно 1 ч (54-176 закрыт ~15:38)",
     "WIN = '2026-10-23T16:30'  # окно 1 ч (54-177 закрыт ~16:3x)"),
    # 4) LPN-заголовок
    ("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_177 (база 15:30, окно 1 ч) =====",
     "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_178 (база 16:30, окно 1 ч) ====="),
    # 5) load prev_177 -> prev_178 + база-примечание
    ("prev = json.load(open('/tmp/prev_lpn_177.json'))",
     "prev = json.load(open('/tmp/prev_lpn_178.json'))"),
    ("print(f'(база prev_lpn_177: {len(prev)} ключей, 15:30 UTC — +196897/+196911/+196912; реанимирована после WIPE-15)')",
     "print(f'(база prev_lpn_178: {len(prev)} ключей, 16:30 UTC — +196889/+196909/+196913/+196914)')"),
    # 6) save prev_178 -> prev_179
    ("json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_178.json', 'w'))",
     "json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_179.json', 'w'))"),
    ("print(f'>>> prev_lpn_178.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')",
     "print(f'>>> prev_lpn_179.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')"),
    # 7) WATCH +4 новых
    ("196904, 196905, 196906, 196897, 196911, 196912]",
     "196904, 196905, 196906, 196897, 196911, 196912, 196889, 196909, 196913, 196914]"),
    # 8) KNOWN +4 новых
    ("196904, 196905, 196906, 196897, 196911, 196912}",
     "196904, 196905, 196906, 196897, 196911, 196912, 196889, 196909, 196913, 196914}"),
    # 9) thread_summary +4 новых
    ("thread_summary(196912)\nprint('\\n===== КАНОН #48 196411 =====')",
     "thread_summary(196912)\nthread_summary(196889)\nthread_summary(196909)\nthread_summary(196913)\nthread_summary(196914)\nprint('\\n===== КАНОН #48 196411 =====')"),
    # 10) DONE
    ("print('\\nDONE 54-177 PHASE1+2')", "print('\\nDONE 54-178 PHASE1+2')"),
]

for old, new in edits:
    n = src.count(old)
    if n != 1:
        raise SystemExit(f'ANCHOR FAIL (count={n}): {old[:90]!r}')
    src = src.replace(old, new)

ast.parse(src)
open(DST, 'w', encoding='utf-8').write(src)
print(f'OK {DST}: {len(edits)} правок, ast OK')
