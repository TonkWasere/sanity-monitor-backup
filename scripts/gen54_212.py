#!/usr/bin/env python3
# gen54_212.py — цепная генерация rescan54_212_fetch.py
# из rescan54_211c_hourly_fetch.py (штатный час 02:20) для часа 03:20.
# База дельт — prev_lpn_213 (02:20, 54-211-C), выход — prev_lpn_214.
# Строгие REPL: каждый old обязан встретиться ровно 1 раз, иначе падаем.
import py_compile, sys

SRC = '/home/z/my-project/tools/rescan54_211c_hourly_fetch.py'
DST = '/home/z/my-project/tools/rescan54_212_fetch.py'

OLD_HEADER = '''# rescan54_211c_hourly_fetch.py — Task 54-211-C: штатный часовой cron-раунд
# ~02:20 UTC 25.10 (54-211 уже отработан ИНТЕРРАУНДОМ 02:12 параллельным
# экземпляром cron-loop — инцидент двойного запуска Job 472526; оба пуша
# 39c9d25d зелёные, работа не потеряна). Этот прогон закрывает остаток окна:
# 02:12->02:20 (8 мин), база дельт — prev_lpn_212 (02:12, интерраунд,
# git-tracked state_snapshots/). WIPE-29 (29-й откат, окно 01:40-01:55)
# закрыт: creds из MEGA-vault автономно + fetch+reset + prev_lpn_211 из
# снапов 0120 (контроль 16/16 — эталон №250, 9-й подряд). Lite-события
# остатка окна: 02:12 s15 — young ПУСТ (graduated 36), events=0.
# Watch: ★ 196949 3-й час после resume? (54/54); ★ 196984 финал гэп 1? (6/5);
# 196946 (54/54); 196976 (11/11); 196977 (3/3); 196973 (27/27); 196975 арбитр
# (25/25); 196962 stm (4/4); 196875 колизей (82/82); ★ 196956 вырез
# подтвердится? (16/15); ★ 196943 вырезы? (183/181); 196834 гэп 7 (64/57);
# 196838 арена (48/45); young: очередь ПУСТА (graduated 36) — RECONCILE
# свежих createdAt; канон 85-й; Санити 85-й; GG 61-й; ОТС 178; флешмоб
# 140-й; 404 120-й; ТГК 3238?; PAT №79
# (ротации нет; 29 откатов за сутки — ВМ мертвецки болен)'''

NEW_HEADER = '''# rescan54_212_fetch.py — Task 54-212: штатный часовой cron-раунд
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

REPL = [
    (OLD_HEADER, NEW_HEADER),
    ("TS = '20261025_0220'", "TS = '20261025_0320'"),
    ("WIN = '2026-10-25T02:12'  # окно 02:12->02:20 (54-210 закрыт 01:4x; 01:20->02:12 закрыл интерраунд 0212)",
     "WIN = '2026-10-25T02:20'  # окно 02:20->03:20 (штатный час; 02:12->02:20 закрыл 54-211-C)"),
    ("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_212 (база 02:12 — интерраунд 0212, WIPE-29 закрыт, state_snapshots git-tracked) =====",
     "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_213 (база 02:20 — 54-211-C штатный час, state_snapshots git-tracked) ====="),
    ("prev = json.load(open('/tmp/prev_lpn_212.json'))",
     "prev = json.load(open('/tmp/prev_lpn_213.json'))"),
    ("(база prev_lpn_212: {len(prev)} ключей, 02:12 UTC — интерраунд 54-211-B после WIPE-29)",
     "(база prev_lpn_213: {len(prev)} ключей, 02:20 UTC — 54-211-C штатный час)"),
    ("json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_213.json', 'w'))",
     "json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_214.json', 'w'))"),
    (">>> prev_lpn_213.json сохранён", ">>> prev_lpn_214.json сохранён"),
    ("DONE 54-211-C HOURLY PHASE1+2", "DONE 54-212 HOURLY PHASE1+2"),
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
