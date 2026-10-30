#!/usr/bin/env python3
# gen54_216.py — цепная генерация rescan54_216_fetch.py
# из rescan54_215_fetch.py (штатный час 06:20) для часа 07:20.
# База дельт — prev_lpn_217 (06:20, 54-215, state_snapshots git-tracked),
# выход — prev_lpn_218.
# Строгие REPL: каждый old обязан встретиться ровно 1 раз, иначе падаем.
import py_compile, sys

SRC = '/home/z/my-project/tools/rescan54_215_fetch.py'
DST = '/home/z/my-project/tools/rescan54_216_fetch.py'

OLD_HEADER = '''# rescan54_215_fetch.py — Task 54-215: штатный часовой cron-раунд
# ~06:20 UTC 25.10, окно 05:20->06:20, база дельт — prev_lpn_216 (05:20,
# 54-214, state_snapshots git-tracked).
# WIPE-32 (32-й откат ВМ, окно ~05:56-06:10, снова к 71c70b8 ~126 ч
# старья): пойман s15 06:10 lite (tools отсутствовали → тихий скип).
# Recovery АВТОНОМЕН ~2 мин (5-й прогон, рутинный): fetch+reset
# 71c70b8->ab107004 + creds из MEGA-vault (restore_creds_54_96, sha256
# 7f9edd5d = эталон, API 200, ls-remote OK) + helper store GLOBAL +
# vault перезаложен в /tmp/PAT_VAULT_LOCAL.md.
# ПОТЕРИ: lite-строки worklog 05:43/05:55 (RECONCILE ×3 young, 196986 +1)
# не успели в коммит — восстановлены реплеем с пометкой; 196985
# выпущен в graduated ~05:58 (37) — подтвердит s15 06:25.
# Watch: ★ 196986 young? (9/9, s15 05:55 +1); 196987 (9/9); ★ 196949
# 7-й час? (60/60); ★ 196973 (34/34); 196948 (44/44); 196968 (44/44);
# 196975 арбитр (26/26); 196976 (11/11); 196977 (5/5); ★ 196956 вырез
# подтвердится? (16/15); ★ 196943 вырезы? (187/185); 196834 гэп 7
# (66/59); 196984 финал (6/5); канон 89-й; Санити 89-й; GG 65-й;
# ОТС 182; флешмоб 144-й; 404 124-й; ТГК 3238?; PAT №79
# (ротации нет; 32 отката за сутки — ВМ мертвецки болен)'''

NEW_HEADER = '''# rescan54_216_fetch.py — Task 54-216: штатный часовой cron-раунд
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

REPL = [
    (OLD_HEADER, NEW_HEADER),
    ("TS = '20261025_0620'", "TS = '20261025_0720'"),
    ("WIN = '2026-10-25T05:20'  # окно 05:20->06:20 (штатный час; ~05:56-06:10 WIPE-32, s15 06:10 скипнулся — покрыто этим обходом)",
     "WIN = '2026-10-25T06:20'  # окно 06:20->07:20 (штатный час; ~07:05-07:20 WIPE-33, s15 07:10 скипнулся — покрыто этим обходом)"),
    ("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_216 (база 05:20 — 54-214 штатный час, state_snapshots git-tracked) =====",
     "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_217 (база 06:20 — 54-215 штатный час, state_snapshots git-tracked) ====="),
    ("prev = json.load(open('/tmp/prev_lpn_216.json'))",
     "prev = json.load(open('/tmp/prev_lpn_217.json'))"),
    ("(база prev_lpn_216: {len(prev)} ключей, 05:20 UTC — 54-214 штатный час)",
     "(база prev_lpn_217: {len(prev)} ключей, 06:20 UTC — 54-215 штатный час)"),
    ("json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_217.json', 'w'))",
     "json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_218.json', 'w'))"),
    (">>> prev_lpn_217.json сохранён", ">>> prev_lpn_218.json сохранён"),
    ("thread_summary(196986)\nthread_summary(196987)\nthread_summary(196985)",
     "thread_summary(196986)\nthread_summary(196987)"),
    ("DONE 54-215 HOURLY PHASE1+2", "DONE 54-216 HOURLY PHASE1+2"),
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
