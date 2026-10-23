# derive_181.py — генерация tools/rescan54_181_fetch.py из rescan54_180_fetch.py
# 11 правок: шапка (раунд 181, окно 19:30->20:30, БЕЗ WIPE — 2-й чистый час, HEAD c0c121a4,
# развёрнута линия молодых тредов SNAP15/SNAP35, watch №220 + молодые 196919-196921/196923/196925
# из young-очереди + 196922/196924, PAT №55), TS 1930->2030, WIN 18:30->19:30,
# prev_181 load/заголовок/база, prev_182 save, WATCH/KNOWN/резюме +7, DONE 54-181
import ast

SRC = '/home/z/my-project/tools/rescan54_180_fetch.py'
DST = '/home/z/my-project/tools/rescan54_181_fetch.py'

src = open(SRC, encoding='utf-8').read()

edits = [
    # 1) шапка
    ("# rescan54_180_fetch.py — Task 54-180: часовой cron-раунд ~19:28 UTC 23.10 (WIPE-16:\n"
     "# 9-Й ОТКАТ ВМ после 7 чистых часов — диск снова 71c70b83 от 19.10, creds DEAD, bundle\n"
     "# НЕТ, /tmp снесён, гэп 91.8 ч; вслепую ~4 мин: stash wipe16-artifacts-1928 → fetch →\n"
     "# ff-only 7e92ed99 (0 потерь, 54-179 уже в remote) → restore_creds_54_96.py (эталон\n"
     "# 7f9edd5d, API 200) → revive_prev_180.py: 91/91 из TS1830-снапов, sanity 21/23\n"
     "# (196832=221 верно; 196916 дыра: выпал из WATCH при генерации 178-го — урок 54-88).\n"
     "# Окно 1 ч: 18:30->19:30 (54-179 закрыт ~18:3x).\n"
     "# Watch-list из №219: 196911 выдыхание подтверждено? (+4 4-й час); 196889/196907\n"
     "# фидбек-пара гэп-3 растёт?; stm-твинк-волна 3 NEW продолжение?; 196916 возврат в\n"
     "# индекс?; 196887 финал?; 196905/196904 рецидив?; 196834 8-й вырез?; Crios ~23 ч;\n"
     "# @Рупоры ~23-й; Санити 53-й; GG 28-й; канон 52-й; 404 88-й; ОТС-итоги X+3 (~146 ч);\n"
     "# флешмоб ~108-й; ТГК 3236?; спектрум 26+ ч; PAT №54",
     "# rescan54_181_fetch.py — Task 54-181: часовой cron-раунд ~20:28 UTC 23.10 (БЕЗ WIPE —\n"
     "# 2-й чистый час после WIPE-16; HEAD c0c121a4 = origin = backup; healthcheck 12/12\n"
     "# ЗДОРОВ; 20:2x UTC развёрнута ЛИНИЯ МОЛОДЫХ ТРЕДОВ по решению автора: SNAP15\n"
     "# :10/:25/:40/:55 + SNAP35 :35 (tools/snap15_young.py + tools/snapnew35.py,\n"
     "# young-очередь 196917-196925, GIT_AUTOMATION.md «Линия молодых тредов»).\n"
     "# Окно 1 ч: 19:30->20:30 (54-180 закрыт ~19:3x).\n"
     "# Watch-list из №220: ★ 196911 6-й час? модерация?; ★ 196918 вырез-волна в\n"
     "# тех-помощь?; ★ 196916 OlderS 3-й час?; ★ stm-волна 3-й час?; 196907/196889\n"
     "# фидбек-пара гэп-3; 196897 гэп-1; 196887 мёртв?; 196834 8-й вырез?; молодые из\n"
     "# young-линии (196919 гэп с рождения 8/7; 196918 гэп 9/8); канон 54-й; Санити 55-й;\n"
     "# GG 30-й; ОТС 148; флешмоб 110-Й; 404 90-Й; ТГК 3236?; Crios 24-й час?; PAT №55"),
    # 2) TS
    ("TS = '20261023_1930'", "TS = '20261023_2030'"),
    # 3) WIN
    ("WIN = '2026-10-23T18:30'  # окно 1 ч (54-179 закрыт ~18:3x)",
     "WIN = '2026-10-23T19:30'  # окно 1 ч (54-180 закрыт ~19:3x)"),
    # 4) LPN-заголовок
    ("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_180 (база 18:30, окно 1 ч) =====",
     "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_181 (база 19:30, окно 1 ч) ====="),
    # 5) load prev_180 -> prev_181
    ("prev = json.load(open('/tmp/prev_lpn_180.json'))",
     "prev = json.load(open('/tmp/prev_lpn_181.json'))"),
    # 6) база-примечание
    ("print(f'(база prev_lpn_180: {len(prev)} ключей, 18:30 UTC — +196915/+196917/+196918; реанимирована после WIPE-16, 196916 дыра закрыта)')",
     "print(f'(база prev_lpn_181: {len(prev)} ключей, 19:30 UTC — +196922/+196924/+196916-возврат)')"),
    # 7) save prev_181 -> prev_182
    ("json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_181.json', 'w'))",
     "json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_182.json', 'w'))"),
    ("print(f'>>> prev_lpn_181.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')",
     "print(f'>>> prev_lpn_182.json сохранён: {len(cur_lpn)} ключей; дельт: {len(deltas)}')"),
    # 8) WATCH +7 (196922/196924 из №220 + молодые из young-линии)
    ("196909, 196913, 196914, 196915, 196916, 196917, 196918]",
     "196909, 196913, 196914, 196915, 196916, 196917, 196918, 196922, 196924, 196919, 196920, 196921, 196923, 196925]"),
    # 9) KNOWN +7
    ("196909, 196913, 196914, 196915, 196916, 196917, 196918}",
     "196909, 196913, 196914, 196915, 196916, 196917, 196918, 196922, 196924, 196919, 196920, 196921, 196923, 196925}"),
    # 10) thread_summary +7
    ("thread_summary(196918)\nprint('\\n===== КАНОН #48 196411 =====')",
     "thread_summary(196918)\nthread_summary(196922)\nthread_summary(196924)\nthread_summary(196919)\n"
     "thread_summary(196920)\nthread_summary(196921)\nthread_summary(196923)\nthread_summary(196925)\n"
     "print('\\n===== КАНОН #48 196411 =====')"),
    # 11) DONE
    ("print('\\nDONE 54-180 PHASE1+2')", "print('\\nDONE 54-181 PHASE1+2')"),
]

for old, new in edits:
    n = src.count(old)
    if n != 1:
        raise SystemExit(f'ANCHOR FAIL (count={n}): {old[:90]!r}')
    src = src.replace(old, new)

ast.parse(src)
open(DST, 'w', encoding='utf-8').write(src)
print(f'OK {DST}: {len(edits)} правок, ast OK')
