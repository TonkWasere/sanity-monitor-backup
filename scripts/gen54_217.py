#!/usr/bin/env python3
# gen54_217.py — цепная генерация rescan54_217_fetch.py
# из rescan54_216_fetch.py (штатный час 07:20) для часа 08:20.
# База дельт — prev_lpn_218 (07:20, 54-216, state_snapshots git-tracked),
# выход — prev_lpn_219.
# Строгие REPL: каждый old обязан встретиться ровно 1 раз, иначе падаем.
import py_compile, sys

SRC = '/home/z/my-project/tools/rescan54_216_fetch.py'
DST = '/home/z/my-project/tools/rescan54_217_fetch.py'

OLD_HEADER = '''# rescan54_216_fetch.py — Task 54-216: штатный часовой cron-раунд
# ~07:20 UTC 25.10, окно 06:20->07:20, база дельт — prev_lpn_217 (06:20,
# 54-215, state_snapshots git-tracked).
# WIPE-33 (33-й откат ВМ, окно ~07:05-07:20, снова к 71c70b8 ~126 ч
# старья): пойман s15 07:10 lite (tools отсутствовали → тихий скип).
# Recovery АВТОНОМЕН ~3 мин (6-й прогон, рутинный): fetch+reset
# 71c70b8->81ff6cd5 + creds из MEGA-vault (restore_creds_54_96, sha256
# 7f9edd5d = эталон, API 200, ls-remote OK) + helper store GLOBAL +
# vault перезаложен; prev_lpn_217 из state_snapshots -> /tmp.
# ПОТЕРИ: lite-строки worklog 06:40/06:55 (re-reconcile young 196986/987
# после WIPE-32; 196986 +1 15/15->16/16) не успели в коммит —
# восстановлены реплеем с пометкой.
# Watch: ★ 196986 stm-сборище? (16/16, young TTL ~07:20); 196987 (9/9,
# TTL ~07:36); ★ 196948 ВЫРЕЗ #41 — чистка продолжится? (44/43);
# ★ 196949 пауза 2-й час? (60/60); ★ 196984 U2F жива? (11/10);
# 196973 (34/34); 196968 (44/44); 196975 арбитр (26/26); 196976 (11/11);
# 196977 (5/5); ★ 196956 вырез (16/15); ★ 196943 вырезы? (190/188);
# 196834 гэп 7 (66/59); канон 90-й; Санити 90-й; GG 66-й; ОТС 183;
# флешмоб 145-й; 404 125-й; ТГК 3238? (тишина 17-й час); PAT №79
# (ротации нет; 33 отката за сутки — ВМ мертвецки болен)'''

NEW_HEADER = '''# rescan54_217_fetch.py — Task 54-217: штатный часовой cron-раунд
# ~08:20 UTC 25.10, окно 07:20->08:20, база дельт — prev_lpn_218 (07:20,
# 54-216, state_snapshots git-tracked).
# WIPE-34 (34-й откат ВМ, окно ~07:50-08:20, снова к 71c70b8 ~126 ч
# старья): пойманы s15 07:55/08:10 lite (tools отсутствовали → тихие
# скипы ×2; s35 07:35 и s15 07:40 успели до вайпа).
# Recovery АВТОНОМЕН ~2 мин (7-й прогон, рутинный): fetch+reset
# 71c70b8->826aa192 + creds из MEGA-vault (restore_creds_54_96, sha256
# 7f9edd5d = эталон, API 200, ls-remote OK) + helper store GLOBAL +
# vault перезаложен; prev_lpn_218 из state_snapshots -> /tmp.
# ПОТЕРИ: lite-строки worklog 07:35 (s35 NEW 196988) / 07:40 (s15
# RECONCILE ×2: 196989 5/5, 196990 4/4) не успели в коммит —
# восстановлены реплеем с пометкой.
# Watch: ★ 196988 «Читеры» (3/3, young); ★ 196989 stm «Накипело!» (5/5,
# young); ★ 196990 «Доставка П/Р/П» (4/4, young — резонанс?); ★ 196986
# stm-сборище (17/17, из young); 196987 (9/9); ★ 196974 арена — разгон
# продолжится? (27/27); ★ 196949 пауза 3-й час? (60/60); ★ 196948 ВЫРЕЗ
# #41 (44/43); 196984 (13/12); 196975 (28/28); 196943 гэп 2 (191/189);
# 196834 гэп 7 (66/59); канон 91-й; Санити 91-й; GG 67-й; ОТС 184;
# флешмоб 146-й; 404 126-й; ТГК 3238? (тишина 18-й час); PAT №80
# (ротации нет; 34 отката за сутки — ВМ мертвецки болен)'''

REPL = [
    (OLD_HEADER, NEW_HEADER),
    ("TS = '20261025_0720'", "TS = '20261025_0820'"),
    ("WIN = '2026-10-25T06:20'  # окно 06:20->07:20 (штатный час; ~07:05-07:20 WIPE-33, s15 07:10 скипнулся — покрыто этим обходом)",
     "WIN = '2026-10-25T07:20'  # окно 07:20->08:20 (штатный час; ~07:50-08:20 WIPE-34, s15 07:55/08:10 скипнулись — покрыто этим обходом)"),
    ("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_217 (база 06:20 — 54-215 штатный час, state_snapshots git-tracked) =====",
     "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_218 (база 07:20 — 54-216 штатный час, state_snapshots git-tracked) ====="),
    ("prev = json.load(open('/tmp/prev_lpn_217.json'))",
     "prev = json.load(open('/tmp/prev_lpn_218.json'))"),
    ("(база prev_lpn_217: {len(prev)} ключей, 06:20 UTC — 54-215 штатный час)",
     "(база prev_lpn_218: {len(prev)} ключей, 07:20 UTC — 54-216 штатный час)"),
    ("json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_218.json', 'w'))",
     "json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_219.json', 'w'))"),
    (">>> prev_lpn_218.json сохранён", ">>> prev_lpn_219.json сохранён"),
    ("WATCH = [196986, 196987, 196985,",
     "WATCH = [196988, 196989, 196990, 196986, 196987, 196985,"),
    ("196979, 196982, 196983, 196984, 196985, 196986, 196987, 196899, 131836, 196778}",
     "196979, 196982, 196983, 196984, 196985, 196986, 196987, 196988, 196989, 196990, 196899, 131836, 196778}"),
    ("thread_summary(196986)\nthread_summary(196987)",
     "thread_summary(196988)\nthread_summary(196989)\nthread_summary(196990)\nthread_summary(196986)"),
    ("DONE 54-216 HOURLY PHASE1+2", "DONE 54-217 HOURLY PHASE1+2"),
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
