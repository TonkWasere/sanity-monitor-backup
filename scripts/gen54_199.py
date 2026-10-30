#!/usr/bin/env python3
# gen54_199.py — цепная генерация rescan54_199_fetch.py из rescan54_198_fetch.py
# Строгие REPL: каждый old обязан встретиться ровно 1 раз, иначе падаем.
import py_compile, sys

SRC = '/home/z/my-project/tools/rescan54_198_fetch.py'
DST = '/home/z/my-project/tools/rescan54_199_fetch.py'

OLD_HEADER = '''# rescan54_198_fetch.py — Task 54-198: часовой cron-раунд ~13:20 UTC 24.10
# (окно 12:20->13:20; 54-197 закрыт 12:40 коммитом 650c48da). WIPE-27 13:1x —
# СЕМНАДЦАТЫЙ откат ВМ за сутки (снова к 71c70b8): отбита хирургией часового
# раунда 13:2x (checkout stale + fetch + ff-merge 71c70b8->650c48da + vault
# из MEGA sha256 7f9edd5d СОВПАЛ API 200 + creds 600 + helper=store +
# prev_lpn_198 из снапов 1220: 132 ключа, контроль 23/24; 196425 132/125 —
# снап авторитетнее, +1 в самом окне обхода). Lite-строки 12:35/12:44/12:55
# восстановлены в worklog с пометкой ВОССТАНОВЛЕНО; 13:10 lite skipped
# (WIPE-27). SNAP15 12:44: стейт усечён (pre active=1) — RECONCILE-ADD ×5,
# выпуск 196950/196951 (TTL 2h); 12:55: 196960 +4 (11/11), 196959 +2 (15/13).
# Watch: ★ 196943 6-я волна/вырезы? (123/121); ★ 196959 вырезы vs рост?
# (15/13); ★ 196960 stm-разгон? (11/11); 196952 (27/27); 196953-956 young;
# ★ 196902 продолжение вспышки? (43/43); ★ 196889/196907 разморозка?;
# 196946 6-й час? (30/30); 131836 #194+?; 196778 #61+?; канон 72-й; Санити
# 72-й; GG 48-й; ОТС 165; флешмоб 127-й; 404 107-й; ТГК 3237?; PAT №72
# (ротации нет; 17 откатов за сутки — ВМ мертвецки болен)'''

NEW_HEADER = '''# rescan54_199_fetch.py — Task 54-199: часовой cron-раунд ~14:20 UTC 24.10
# (окно 13:20->14:20; 54-198 закрыт 13:31 коммитом 9bded97f). WIPE-28 13:4x —
# ВОСЕМНАДЦАТЫЙ откат ВМ за сутки (снова к 71c70b8): отбита хирургией часового
# раунда 14:2x (checkout stale + fetch + ff-merge 71c70b8->9bded97f + vault
# из MEGA sha256 7f9edd5d СОВПАЛ API 200 + creds 600 + helper=store +
# prev_lpn_199 из снапов 1320: 133 ключа, контроль 31/31 — эталон №238).
# Lite: SNAP35 13:35 тихо (new=0); SNAP15 13:40 тихо — active=4
# (196955/1956/1959/1960), graduated=32; 13:55/14:10 lite skipped (WIPE-28).
# Watch: ★ 196943 7-я волна/вырезы? (134/132); ★ 196902 3-й час вспышки?
# (52/52); ★ 196889 продолжение разморозки? (89/85); ★ 196959/196960
# young-рост? (15/13, 11/11); 196953 (17/17); ★ 196946 7-й час? (35/35);
# 131836 #194+?; 196778 #61+?; канон 73-й; Санити 73-й; GG 49-й; ОТС 166;
# флешмоб 128-й; 404 108-й; ТГК 3237?; PAT №72
# (ротации нет; 18 откатов за сутки — ВМ мертвецки болен)'''

REPL = [
    (OLD_HEADER, NEW_HEADER),
    ("TS = '20261024_1320'", "TS = '20261024_1420'"),
    ("WIN = '2026-10-24T12:20'  # окно 1 ч (54-197 закрыт 12:40)",
     "WIN = '2026-10-24T13:20'  # окно 1 ч (54-198 закрыт 13:31)"),
    ("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_198 (база 12:20 — восстановлена из git-снапов после WIPE-27) =====",
     "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_199 (база 13:20 — восстановлена из git-снапов после WIPE-28) ====="),
    ("prev = json.load(open('/tmp/prev_lpn_198.json'))",
     "prev = json.load(open('/tmp/prev_lpn_199.json'))"),
    ("(база prev_lpn_198: {len(prev)} ключей, 12:20 UTC — раунд 54-197, восстановлена после WIPE-27)",
     "(база prev_lpn_199: {len(prev)} ключей, 13:20 UTC — раунд 54-198, восстановлена после WIPE-28)"),
    ("open('/tmp/prev_lpn_199.json', 'w'))", "open('/tmp/prev_lpn_200.json', 'w'))"),
    (">>> prev_lpn_199.json сохранён", ">>> prev_lpn_200.json сохранён"),
    ("DONE 54-198 PHASE1+2", "DONE 54-199 PHASE1+2"),
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
