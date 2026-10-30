# derive_179.py — генерация tools/rescan54_179_fetch.py из rescan54_178_fetch.py
# 9 правок: шапка (раунд 179, окно 17:30->18:30, 7-й час без WIPE, watch №218, PAT №53),
# TS 1730->1830, WIN 16:30->17:30, prev_179 load/заголовок/база, prev_180 save, DONE 54-179
import ast

SRC = '/home/z/my-project/tools/rescan54_178_fetch.py'
DST = '/home/z/my-project/tools/rescan54_179_fetch.py'

src = open(SRC, encoding='utf-8').read()

edits = [
    # 1) шапка
    ("# rescan54_178_fetch.py — Task 54-178: часовой cron-раунд ~17:28 UTC 23.10 (БЕЗ WIPE —\n"
     "# 6-й чистый час подряд; HEAD 70cbbe20 = origin = backup; healthcheck 12/12 ЗДОРОВ).\n"
     "# Окно 1 ч: 16:30->17:30 (54-177 закрыт ~16:3x; WIPE-15 вслепую закрыт за ~3 мин).\n"
     "# Watch-list из №217: 196911 перс-магазин 3-й час взрыва (+29/+28 во 2-м, 51/50)?;\n"
     "# 196905 ретро-скрытие #23 — продолжение задних резок?; 196889 ОТС «Празднество» гэп-3\n"
     "# растёт?; 196834 8-й вырез?; 196887 залив +1 не мёртв — растёт?; 196897 судьба\n"
     "# (1 вырез)?; 196902 ожил — растёт?; Crios ~21 ч; @Рупоры ~21-й; Санити 51-й; GG 26-й;\n"
     "# канон 50-й; 404 86-й; ОТС-итоги X+3 (~144 ч); флешмоб ~106-й; ТГК 3235;\n"
     "# спектрум 24+ ч; PAT №52",
     "# rescan54_179_fetch.py — Task 54-179: часовой cron-раунд ~18:28 UTC 23.10 (БЕЗ WIPE —\n"
     "# 7-й чистый час подряд; HEAD 4369be29 = origin = backup; healthcheck 12/12 ЗДОРОВ).\n"
     "# Окно 1 ч: 17:30->18:30 (54-178 закрыт ~17:3x).\n"
     "# Watch-list из №218: 196911 магазин 4-й час? снос-волна модерации?; 196889 ОТС-тред\n"
     "# гэп-3 растёт?; 196907 оф. фидбек Празднества: гэп-3 растёт? фидбек-волна?; 196913 мем\n"
     "# / 196916 скандал OlderS развитие; 196887 финал?; 196905 рецидив?; 196834 8-й вырез?;\n"
     "# Crios ~22 ч; @Рупоры ~22-й; Санити 52-й; GG 27-й; канон 51-й; 404 87-й;\n"
     "# ОТС-итоги X+3 (~145 ч); флешмоб ~107-й; ТГК 3236?; Празднество: фидбек-волна;\n"
     "# спектрум 25+ ч; PAT №53"),
    # 2) TS
    ("TS = '20261023_1730'", "TS = '20261023_1830'"),
    # 3) WIN
    ("WIN = '2026-10-23T16:30'  # окно 1 ч (54-177 закрыт ~16:3x)",
     "WIN = '2026-10-23T17:30'  # окно 1 ч (54-178 закрыт ~17:3x)"),
    # 4) LPN-заголовок
    ("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_178 (база 16:30, окно 1 ч) =====",
     "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_179 (база 17:30, окно 1 ч) ====="),
    # 5) load prev_178 -> prev_179
    ("prev = json.load(open('/tmp/prev_lpn_178.json'))",
     "prev = json.load(open('/tmp/prev_lpn_179.json'))"),
    # 6) база-примечание
    ("print(f'(база prev_lpn_178: {len(prev)} ключей, 16:30 UTC — +196889/+196909/+196913/+196914)')",
     "print(f'(база prev_lpn_179: {len(prev)} ключей, 17:30 UTC — +196907/+196916)')"),
    # 7) save prev_179 -> prev_180
    ("json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_179.json', 'w'))",
     "json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_180.json', 'w'))"),
    ("print(f'>>> prev_lpn_179.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')",
     "print(f'>>> prev_lpn_180.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')"),
    # 8) DONE
    ("print('\\nDONE 54-178 PHASE1+2')", "print('\\nDONE 54-179 PHASE1+2')"),
]

for old, new in edits:
    n = src.count(old)
    if n != 1:
        raise SystemExit(f'ANCHOR FAIL (count={n}): {old[:90]!r}')
    src = src.replace(old, new)

ast.parse(src)
open(DST, 'w', encoding='utf-8').write(src)
print(f'OK {DST}: {len(edits)} правок, ast OK')
