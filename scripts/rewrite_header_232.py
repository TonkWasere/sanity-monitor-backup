# rewrite_header_232.py — заменяет шапку rescan54_232_fetch.py (строки 1-12) на заголовок 54-232
p = 'tools/rescan54_232_fetch.py'
L = open(p, encoding='utf-8').read().split('\n')
assert L[12].startswith('import json'), f'line13 unexpected: {L[12]!r}'
new = [
    '# rescan54_232_fetch.py — Task 54-232: штатный часовой cron-раунд (Task ID 54-232)',
    '# ~23:20 UTC 25.10, окно 22:20->23:20, база дельт — prev_lpn_233 (22:30, 54-231,',
    '# 193 кл). Окно: форензика «бесследных» тиков :25 (54-23: шедулер ЗАПУСКАЛ,',
    '# run_count=6; агент-ходы потеряны в часовой петле 21:25 и 22:25; детектор',
    '# TICK-LOST v2 в snap15 шаг 0, живой FP v1 классифицирован); выпуск s15 23:10 x3',
    '# (197023/24/25 -> graduated 70, young 5->2). Watch: * офиц. итоги ОТС (9-й день',
    '# без итогов; ТГК #3241? Steam? news?); * 197021 судьба оригинала (156/156 гэп 2',
    '# — гэп 2->3? LOCK? VANISH?); * 197028 «Брелок-счётчик» (22:14Z, young, mlr-твинк',
    '# 3-е появление — OP/паттерн); 197026 рост; VANISH-эхо 197022; 196889 гэп 5->6?;',
    '# канон 106-й час; Санити 82-й; ТГК #3241?; fan/spectrum #7986+? PAT №86 жив',
]
open(p, 'w', encoding='utf-8').write('\n'.join(new + L[12:]))
print(f'HEADER-REWRITTEN: {len(new)} новых строк, всего {len(new) + len(L) - 12}')
