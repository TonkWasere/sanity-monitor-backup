# derive_182.py — генерация tools/rescan54_182_fetch.py из rescan54_181_fetch.py
# 11 правок: шапка (раунд 182, окно 20:30->21:30, БЕЗ WIPE — 3-й чистый час, HEAD f22811d0,
# cron пересоздан 462533->472526 с шагом 1b ВНЕШНИЕ ИСТОЧНИКИ ext_sources.py, консолидация
# дубля, ВК-стена открыта 54-21-ext-c, SNAP15 quiet + 196920 ВЫРЕЗ 21:11, watch №221,
# PAT №56), TS 2030->2130, WIN 19:30->20:30, prev_182 load/заголовок/база, prev_183 save,
# WATCH/KNOWN/резюме +196907 (закрытие дыры KNOWN — урок 54-88), DONE 54-182
import ast

SRC = '/home/z/my-project/tools/rescan54_181_fetch.py'
DST = '/home/z/my-project/tools/rescan54_182_fetch.py'

src = open(SRC, encoding='utf-8').read()

edits = [
    # 1) шапка
    ("# rescan54_181_fetch.py — Task 54-181: часовой cron-раунд ~20:28 UTC 23.10 (БЕЗ WIPE —\n"
     "# 2-й чистый час после WIPE-16; HEAD c0c121a4 = origin = backup; healthcheck 12/12\n"
     "# ЗДОРОВ; 20:2x UTC развёрнута ЛИНИЯ МОЛОДЫХ ТРЕДОВ по решению автора: SNAP15\n"
     "# :10/:25/:40/:55 + SNAP35 :35 (tools/snap15_young.py + tools/snapnew35.py,\n"
     "# young-очередь 196917-196925, GIT_AUTOMATION.md «Линия молодых тредов»).\n"
     "# Окно 1 ч: 19:30->20:30 (54-180 закрыт ~19:3x).\n"
     "# Watch-list из №220: ★ 196911 6-й час? модерация?; ★ 196918 вырез-волна в\n"
     "# тех-помощь?; ★ 196916 OlderS 3-й час?; ★ stm-волна 3-й час?; 196907/196889\n"
     "# фидбек-пара гэп-3; 196897 гэп-1; 196887 мёртв?; 196834 8-й вырез?; молодые из\n"
     "# young-линии (196919 гэп с рождения 8/7; 196918 гэп 9/8); канон 54-й; Санити 55-й;\n"
     "# GG 30-й; ОТС 148; флешмоб 110-Й; 404 90-Й; ТГК 3236?; Crios 24-й час?; PAT №55",
     "# rescan54_182_fetch.py — Task 54-182: часовой cron-раунд ~21:2x UTC 23.10 (БЕЗ WIPE —\n"
     "# 3-й чистый час; HEAD f22811d0 = origin = backup; healthcheck 12/12 ЗДОРОВ;\n"
     "# cron пересоздан: 462533 -> 472526 с шагом 1b ВНЕШНИЕ ИСТОЧНИКИ tools/ext_sources.py —\n"
     "# ТГК stalzone+spectrum_zone, Steam RSS RU/EN, VK-статьи + ВК-СТЕНА vk.com (пробел\n"
     "# закрыт 54-21-ext-c; дубль sources_hourly.py выведен консолидацией 54-181).\n"
     "# Окно 1 ч: 20:30->21:30 (54-181 закрыт ~20:4x).\n"
     "# Watch-list из №221: ★ 196911 7-й час взрыв +8?; ★ 196918 вырез-волна в\n"
     "# тех-помощь?; ★ 196916 OlderS 4-й час?; ★ stm-волна 4-й час?; 196907/196889\n"
     "# фидбек-пара (196907 теперь в WATCH/KNOWN — дыра derive_179 закрыта); молодые\n"
     "# 196919/196920 гэп-1, 196918 гэп 9/8; канон 55-й; Санити 56-й; GG 31-й; ОТС 149;\n"
     "# флешмоб 111-й; 404 91-й; ТГК 3236?; Crios 25-й час?; PAT №56"),
    # 2) TS
    ("TS = '20261023_2030'", "TS = '20261023_2130'"),
    # 3) WIN
    ("WIN = '2026-10-23T19:30'  # окно 1 ч (54-180 закрыт ~19:3x)",
     "WIN = '2026-10-23T20:30'  # окно 1 ч (54-181 закрыт ~20:4x)"),
    # 4) LPN-заголовок
    ("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_181 (база 19:30, окно 1 ч) =====",
     "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_182 (база 20:30, окно 1 ч) ====="),
    # 5) load prev_181 -> prev_182
    ("prev = json.load(open('/tmp/prev_lpn_181.json'))",
     "prev = json.load(open('/tmp/prev_lpn_182.json'))"),
    # 6) база-примечание
    ("print(f'(база prev_lpn_181: {len(prev)} ключей, 19:30 UTC — +196922/+196924/+196916-возврат)')",
     "print(f'(база prev_lpn_182: {len(prev)} ключей, 20:30 UTC — +196919/+196920/+196921/+196923/+196925)')"),
    # 7) save prev_182 -> prev_183
    ("json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_182.json', 'w'))",
     "json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_183.json', 'w'))"),
    ("print(f'>>> prev_lpn_182.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')",
     "print(f'>>> prev_lpn_183.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')"),
    # 8) WATCH +196907 (закрытие дыры KNOWN derive_179)
    ("196919, 196920, 196921, 196923, 196925]",
     "196919, 196920, 196921, 196923, 196925, 196907]"),
    # 9) KNOWN +196907
    ("196919, 196920, 196921, 196923, 196925}",
     "196919, 196920, 196921, 196923, 196925, 196907}"),
    # 10) thread_summary +196907 (после 196889 — фидбек-пара)
    ("thread_summary(196889)\nthread_summary(196909)",
     "thread_summary(196889)\nthread_summary(196907)\nthread_summary(196909)"),
    # 11) DONE
    ("print('\\nDONE 54-181 PHASE1+2')", "print('\\nDONE 54-182 PHASE1+2')"),
]

for old, new in edits:
    n = src.count(old)
    if n != 1:
        raise SystemExit(f'ANCHOR FAIL (count={n}): {old[:90]!r}')
    src = src.replace(old, new)

ast.parse(src)
open(DST, 'w', encoding='utf-8').write(src)
print(f'OK {DST}: {len(edits)} правок, ast OK')
