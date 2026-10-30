#!/usr/bin/env python3
# gen54_213.py — цепная генерация rescan54_213_fetch.py
# из rescan54_212_fetch.py (штатный час 03:20) для часа 04:20.
# База дельт — prev_lpn_214 (03:20, 54-212; восстановлен из Хранилища
# после WIPE-30), выход — prev_lpn_215.
# Строгие REPL: каждый old обязан встретиться ровно 1 раз, иначе падаем.
import py_compile, sys

SRC = '/home/z/my-project/tools/rescan54_212_fetch.py'
DST = '/home/z/my-project/tools/rescan54_213_fetch.py'

OLD_HEADER = '''# rescan54_212_fetch.py — Task 54-212: штатный часовой cron-раунд
# ~03:20 UTC 25.10, окно 02:20->03:20, база дельт — prev_lpn_213 (02:20,
# 54-211-C, git-tracked state_snapshots/). Предыдущая сессия агента
# исчерпала контекст СРАЗУ ПОСЛЕ SNAP15 03:11 lite — прогон тихий (young
# ПУСТ, graduated 36; NEW 0 — в created30 нет тредов новее 196984 00:05;
# журнал тих с 02:11:25), работа не потеряна: снапы 0220 и стейт на диске,
# git чист на 90bd32dc (оба remote), раунд продолжается без дублей.
# Watch: ★ 196949 4-й час после resume? (56/56); ★ 196984 финал гэп 1? (6/5);
# 196946 (54/54); 196976 (11/11); 196977 (5/5); 196973 (27/27); 196975 арбитр
# (25/25); 196962 stm (4/4); 196875 колизей (82/82); ★ 196956 вырез
# подтвердится? (16/15); ★ 196943 вырезы? (183/181); 196834 гэп 7 (65/58);
# 196838 арена (48/45); young: очередь ПУСТА (graduated 36) — RECONCILE
# свежих createdAt; канон 86-й; Санити 86-й; GG 62-й; ОТС 179; флешмоб
# 141-й; 404 121-й; ТГК 3238?; PAT №79
# (ротации нет; 29 откатов за сутки — ВМ мертвецки болен)'''

NEW_HEADER = '''# rescan54_213_fetch.py — Task 54-213: штатный часовой cron-раунд
# ~04:20 UTC 25.10, окно 03:20->04:20, база дельт — prev_lpn_214 (03:20,
# 54-212; восстановлен из git-Хранилища state_snapshots одной командой).
# WIPE-30 (30-й откат ВМ, окно 03:40-03:55, снова к 71c70b8 ~124 ч
# старья): пойман s15 03:55 lite (tools отсутствовали → тихий скип;
# 04:10 s15 тоже скип). Recovery по чек-листу АВТОНОМЕН ~3 мин: fetch+reset
# 71c70b8->15b5a5f7 + prev_lpn_214 из Хранилища (restore_state_from_repo,
# 153 кл, без rebuild-хирургии) + creds из MEGA-vault (sha256 7f9edd5d =
# эталон, API 200) + helper store + backups. Хранилище автора работает.
# Lite-события окна: s35 03:39 тихо (candidates=0), s15 03:40 тихо, далее
# WIPE — s15 03:55/04:10 skipped (покрыто этим обходом).
# Watch: ★ 196949 5-й час после resume? (57/57); ★ 196984 финал гэп 1? (6/5);
# 196946 (55/55); 196976 (11/11); 196977 (5/5); 196973 (29/29); 196975 арбитр
# (25/25); 196962 stm (4/4); 196875 колизей (82/82); ★ 196956 вырез
# подтвердится? (16/15); ★ 196943 вырезы? (183/181); 196834 гэп 7 (66/59);
# 196838 арена (48/45); young: очередь ПУСТА (graduated 36) — RECONCILE
# свежих createdAt; канон 87-й; Санити 87-й; GG 63-й; ОТС 180; флешмоб
# 142-й; 404 122-й; ТГК 3238?; PAT №79
# (ротации нет; 30 откатов за сутки — ВМ мертвецки болен)'''

REPL = [
    (OLD_HEADER, NEW_HEADER),
    ("TS = '20261025_0320'", "TS = '20261025_0420'"),
    ("WIN = '2026-10-25T02:20'  # окно 02:20->03:20 (штатный час; 02:12->02:20 закрыл 54-211-C)",
     "WIN = '2026-10-25T03:20'  # окно 03:20->04:20 (штатный час; 03:40-03:55 WIPE-30, lite скипались — покрыто этим обходом)"),
    ("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_213 (база 02:20 — 54-211-C штатный час, state_snapshots git-tracked) =====",
     "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_214 (база 03:20 — 54-212 штатный час; восстановлен из Хранилища после WIPE-30) ====="),
    ("prev = json.load(open('/tmp/prev_lpn_213.json'))",
     "prev = json.load(open('/tmp/prev_lpn_214.json'))"),
    ("(база prev_lpn_213: {len(prev)} ключей, 02:20 UTC — 54-211-C штатный час)",
     "(база prev_lpn_214: {len(prev)} ключей, 03:20 UTC — 54-212, восстановлен из Хранилища)"),
    ("json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_214.json', 'w'))",
     "json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_215.json', 'w'))"),
    (">>> prev_lpn_214.json сохранён", ">>> prev_lpn_215.json сохранён"),
    ("DONE 54-212 HOURLY PHASE1+2", "DONE 54-213 HOURLY PHASE1+2"),
]

def main():
    src = open(SRC, encoding='utf-8').read()
    for i, (old, new) in enumerate(REPL, 1):
        n = src.count(old)
        if n != 1:
            print(f'R{i} FAIL: {n} вхождений (нужно 1): {old[:60]!r}')
            return 1
        src = src.replace(old, new)
    open(DST, 'w', encoding='utf-8').write(src)
    py_compile.compile(DST, doraise=True)
    print(f'OK: {DST} сгенерирован, py_compile OK, {len(REPL)} REPL применено')
    return 0

if __name__ == '__main__':
    sys.exit(main())
