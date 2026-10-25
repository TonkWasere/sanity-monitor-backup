#!/usr/bin/env python3
# gen54_215.py — цепная генерация rescan54_215_fetch.py
# из rescan54_214_fetch.py (штатный час 05:20) для часа 06:20.
# База дельт — prev_lpn_216 (05:20, 54-214, state_snapshots git-tracked),
# выход — prev_lpn_217.
# Строгие REPL: каждый old обязан встретиться ровно 1 раз, иначе падаем.
import py_compile, sys

SRC = '/home/z/my-project/tools/rescan54_214_fetch.py'
DST = '/home/z/my-project/tools/rescan54_215_fetch.py'

OLD_HEADER = '''# rescan54_214_fetch.py — Task 54-214: штатный часовой cron-раунд
# ~05:20 UTC 25.10, окно 04:20->05:20, база дельт — prev_lpn_215 (04:20,
# 54-213, state_snapshots git-tracked).
# WIPE-31 (31-й откат ВМ, окно 04:35-04:55, снова к 71c70b8 ~126 ч
# старья): пойман s15 04:55 lite (tools отсутствовали → тихий скип;
# 05:10 s15 тоже скип). Recovery по чек-листу АВТОНОМЕН ~4 мин:
# fetch+reset 71c70b8->68cd73f9 + creds из MEGA-vault (restore_creds_54_96,
# sha256 7f9edd5d = эталон, API 200, ls-remote OK) + helper store GLOBAL +
# vault -> /tmp/PAT_VAULT_LOCAL.md. Хранилище автора работает.
# Lite-события окна: s15 04:25 — 196985 в young-очередь (6, active=1,
# graduated 36); s35 04:35 тихо (KNOWN=193); далее WIPE-31 — s15 04:40
# инициирован, результат не доставлен; 04:55/05:10 skipped (покрыто этим
# обходом).
# Watch: ★ 196949 6-й час после resume? (59/59); ★ 196984 финал гэп 1?
# (6/5); 196946 (55/55); 196976 (11/11); 196977 (5/5); 196973 (33/33);
# 196975 арбитр (25/25); 196962 stm (4/4); 196875 колизей (82/82);
# ★ 196956 вырез подтвердится? (16/15); ★ 196943 вырезы? (183/181);
# 196834 гэп 7 (66/59); 196838 арена (48/45); young: ★ 196985 активный
# (6 в очереди, graduated 36) — 15-мин дельты lite догоняют; канон 88-й;
# Санити 88-й; GG 64-й; ОТС 181; флешмоб 143-й; 404 123-й; ТГК 3238?;
# PAT №79
# (ротации нет; 31 откат за сутки — ВМ мертвецки болен)'''

NEW_HEADER = '''# rescan54_215_fetch.py — Task 54-215: штатный часовой cron-раунд
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

REPL = [
    (OLD_HEADER, NEW_HEADER),
    ("TS = '20261025_0520'", "TS = '20261025_0620'"),
    ("WIN = '2026-10-25T04:20'  # окно 04:20->05:20 (штатный час; 04:35-04:55 WIPE-31, lite 04:40-05:10 скипались — покрыто этим обходом)",
     "WIN = '2026-10-25T05:20'  # окно 05:20->06:20 (штатный час; ~05:56-06:10 WIPE-32, s15 06:10 скипнулся — покрыто этим обходом)"),
    ("WATCH = [196985, 196872, 196871, 196855, 196867, 196865, 196864, 196862, 196838, 196856, 196854,",
     "WATCH = [196986, 196987, 196985, 196872, 196871, 196855, 196867, 196865, 196864, 196862, 196838, 196856, 196854,"),
    ("196979, 196982, 196983, 196984, 196985, 196899, 131836, 196778}",
     "196979, 196982, 196983, 196984, 196985, 196986, 196987, 196899, 131836, 196778}"),
    ("print('\\n===== КЛЮЧЕВЫЕ РЕЗЮМЕ =====')\nthread_summary(196985)",
     "print('\\n===== КЛЮЧЕВЫЕ РЕЗЮМЕ =====')\nthread_summary(196986)\nthread_summary(196987)\nthread_summary(196985)"),
    ("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_215 (база 04:20 — 54-213 штатный час, state_snapshots git-tracked) =====",
     "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_216 (база 05:20 — 54-214 штатный час, state_snapshots git-tracked) ====="),
    ("prev = json.load(open('/tmp/prev_lpn_215.json'))",
     "prev = json.load(open('/tmp/prev_lpn_216.json'))"),
    ("(база prev_lpn_215: {len(prev)} ключей, 04:20 UTC — 54-213 штатный час)",
     "(база prev_lpn_216: {len(prev)} ключей, 05:20 UTC — 54-214 штатный час)"),
    ("json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_216.json', 'w'))",
     "json.dump({str(k): v for k, v in cur_lpn.items()}, open('/tmp/prev_lpn_217.json', 'w'))"),
    (">>> prev_lpn_216.json сохранён", ">>> prev_lpn_217.json сохранён"),
    ("DONE 54-214 HOURLY PHASE1+2", "DONE 54-215 HOURLY PHASE1+2"),
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
