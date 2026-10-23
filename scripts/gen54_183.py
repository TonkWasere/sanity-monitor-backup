#!/usr/bin/env python3
"""gen54_183.py — генератор rescan54_183_fetch.py из rescan54_182_fetch.py
+ bootstrap: /tmp/prev_lpn_183.json из снапов TS 2130 (база 21:30 UTC 23.10),
  т.к. оригинал погиб в вайпе ~22:00 (реанимация 22:2x, HEAD 125a3d90).
"""
import glob
import json
import os
import re

SRC = '/home/z/my-project/tools/rescan54_182_fetch.py'
DST = '/home/z/my-project/tools/rescan54_183_fetch.py'
OUT = '/home/z/my-project/output/evidence_post'
TS_OLD = '20261023_2130'
BASE_TS = '2130'

# --- 1. Bootstrap prev_lpn_183.json из снапов 21:30 ---
base = {}
for fn in sorted(glob.glob(os.path.join(OUT, f'discussion_*_near999999_{TS_OLD}.json'))):
    m = re.match(r'discussion_(\d+)_near999999_' + TS_OLD + r'\.json', os.path.basename(fn))
    if not m:
        continue
    tid = int(m.group(1))
    try:
        d = json.load(open(fn))
        a = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        base[str(tid)] = {'lpn': a.get('lastPostNumber'), 'cc': a.get('commentCount')}
    except Exception as e:
        print(f'skip {tid}: {e}')
json.dump(base, open('/tmp/prev_lpn_183.json', 'w'))
print(f'bootstrap prev_lpn_183.json: {len(base)} ключей из снапов {TS_OLD}')

# --- 2. Генерация rescan54_183 ---
src = open(SRC).read()

# 2a. Header (всё до import json)
new_header = '''# rescan54_183_fetch.py — Task 54-183: часовой cron-раунд ~22:2x UTC 23.10
# (окно сдвинуто вайпом: WIPE ~22:00 унёс /tmp+creds+snap-tools; реанимация 22:2x по
# MEGA-vault автора + GitHub 163 коммитов — HEAD 125a3d90, healthcheck 12/12, детали
# в GIT_AUTOMATION инцидент-логе). Окно 1 ч: 21:30->22:30 (54-182 закрыт 21:28).
# Watch-list из №222: ★ 196926 фармер-кандидат (Snap15: recon 21:40, 9/9); ★ 196928
# разгон +7 (3/3->10/10 @22:55); ★ 196929/196930 новые молодые; ★ 196911 замедление +3;
# 196889 ОТС гэп-4; канон 56-й; Санити 57-й; GG 32-й; ОТС 150; флешмоб 112-й; 404 92-й;
# ТГК 3237?; Crios 26-й час?; PAT №57 (токен восстановлен 22:2x — ротация у автора не сделана)
'''
src = re.sub(r'\A# rescan54_182_fetch\.py.*?(?=import json, os)', new_header, src, flags=re.S)

# 2b. TS / WIN
src = src.replace("TS = '20261023_2130'", "TS = '20261023_2230'")
src = src.replace("WIN = '2026-10-23T20:30'  # окно 1 ч (54-181 закрыт ~20:4x)",
                  "WIN = '2026-10-23T21:30'  # окно 1 ч (54-182 закрыт 21:28)")

# 2c. prev-файлы: сначала выходной (183->184), затем входной (182->183)
src = src.replace("open('/tmp/prev_lpn_183.json', 'w')", "open('/tmp/prev_lpn_184.json', 'w')")
src = src.replace(">>> prev_lpn_183.json сохранён", ">>> prev_lpn_184.json сохранён")
src = src.replace("open('/tmp/prev_lpn_182.json')", "open('/tmp/prev_lpn_183.json')")

# 2d. Подписи LPN-секции
src = src.replace("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_182 (база 20:30, окно 1 ч) =====",
                  "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_183 (база 21:30, из снапов 2130) =====")
src = src.replace("print(f'(база prev_lpn_182: {len(prev)} ключей, 20:30 UTC — +196919/+196920/+196921/+196923/+196925)')",
                  "print(f'(база prev_lpn_183: {len(prev)} ключей, 21:30 UTC — bootstrap из снапов 2130 после вайпа /tmp)')")

# 2e. WATCH + KNOWN: +196926..196930
src = src.replace("196925, 196907]", "196925, 196907, 196926, 196927, 196928, 196929, 196930]")
src = src.replace("196925, 196907}", "196925, 196907, 196926, 196927, 196928, 196929, 196930}")

# 2f. thread_summary: +196926..196930
src = src.replace("thread_summary(196925)\nprint('\\n===== КАНОН #48 196411 =====')",
                  "thread_summary(196925)\nthread_summary(196926)\nthread_summary(196927)\nthread_summary(196928)\nthread_summary(196929)\nthread_summary(196930)\nprint('\\n===== КАНОН #48 196411 =====')")

# 2g. DONE
src = src.replace("print('\\nDONE 54-182 PHASE1+2')", "print('\\nDONE 54-183 PHASE1+2')")

assert "TS = '20261023_2230'" in src and "prev_lpn_184" in src and "196930]" in src
open(DST, 'w').write(src)
print(f'written {DST}: {len(src)} bytes')
