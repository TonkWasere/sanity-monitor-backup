#!/usr/bin/env python3
# gen54_12.py — генератор rescan54_12_fetch.py из rescan54_11_fetch.py (sed-подход прежних раундов)
src = open('/home/z/my-project/tools/rescan54_11_fetch.py', encoding='utf-8').read()

# 1) Новый заголовок
h0 = src.index('#!/usr/bin/env python3')
h1 = src.index('import json, os, urllib.request')
new_hdr = '''#!/usr/bin/env python3
# rescan54_12_fetch.py — Task 54-12: часовой cron-раунд ~12:30 UTC 16.10 (15:30 МСК). Среда жива,
# но creds потеряны при откате ВМ — push pending (коммит bc68f68 ждёт токен автора).
# Дельта 11:30→12:30 UTC ~1 ч. Караул: ОТС старт 15:00 UTC (~2.5 ч, предстартовый всплеск?),
# компенсация (факт? окно до полуночи МСК ~9.5 ч), Тирлист 196532 (cc=170, второй центр гравитации),
# Глеб 196524 (cc=548), ТГК 3206+, Талоны ~45 ч офиц. молчания, 196411 сносы #71+.
#
'''
src = src[:h0] + new_hdr + src[h1:]

# 2) Порог фронт-индекса: всё, что живо с 11:00 UTC
src = src.replace('2026-10-16T08:00', '2026-10-16T11:00')

# 3) Новые треды в обход (после GET 196531)
anchor_get = "get(f'{BASE}/api/discussions/196531?page[near]=999999', f'discussion_196531_near999999_{TS}.json'); time.sleep(1)"
add_gets = anchor_get + "\nget(f'{BASE}/api/discussions/196532?page[near]=999999', f'discussion_196532_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196536?page[near]=999999', f'discussion_196536_near999999_{TS}.json'); time.sleep(1)\nget(f'{BASE}/api/discussions/196533?page[near]=999999', f'discussion_196533_near999999_{TS}.json'); time.sleep(1)"
assert anchor_get in src
src = src.replace(anchor_get, add_gets)

# 4) KNOWN: +196532/196536/196533
old_known_tail = '196529, 196530, 196531, 196496, 196260, 196100, 196258, 196501}'
new_known_tail = '196529, 196530, 196531, 196496, 196260, 196100, 196258, 196501, 196532, 196536, 196533}'
assert old_known_tail in src
src = src.replace(old_known_tail, new_known_tail)

# 5) Базлайны в заголовках секций
repl = [
    ('===== 196524 Глеб (был cc=464) =====', '===== 196524 Глеб (был cc=548) ====='),
    ('===== 196475 Амнистия (был cc=220) =====', '===== 196475 Амнистия (был cc=227) ====='),
    ('===== 196435 Колизей-калибровка (был cc=150) =====', '===== 196435 Колизей-калибровка (был cc=153) ====='),
    ('===== 196496 Простой пример (был cc=68) =====', '===== 196496 Простой пример (был cc=70) ====='),
    ('===== 196516 Соло гемлпей =====', '===== 196516 Соло гемлпей (был cc=22) ====='),
    ('===== 196510 КАЛЛибровка-2 (был cc=21) =====', '===== 196510 КАЛЛибровка-2 (был cc=22) ====='),
    ('===== 196424 ОТС (старт 15:00 UTC ~3.5 ч) =====', '===== 196424 ОТС (старт 15:00 UTC ~2.5 ч) ====='),
    ('===== 196452 Талоны PvE (~44 ч офиц. молчания) =====', '===== 196452 Талоны PvE (~45 ч офиц. молчания) ====='),
    ('===== 196511 Хотфикс (компенсация обещана 16.10; факт/окно ~10.5 ч) =====', '===== 196511 Хотфикс (компенсация обещана 16.10; факт/окно ~9.5 ч) ====='),
]
for a, b in repl:
    assert a in src, a
    src = src.replace(a, b)

# 6) Секции-резюме новых тредов (перед блоком ОТС)
ots_anchor = "print('\\n===== 196424 ОТС"
new_blocks = (
    "print('\\n===== 196532 Тирлист Завозов (был cc=170) =====')\n"
    "thread_summary(196532)\n"
    "print('\\n===== 196536 Смена оружия (был cc=4) =====')\n"
    "thread_summary(196536)\n"
    "print('\\n===== 196533 Американская гитара (был cc=2) =====')\n"
    "thread_summary(196533)\n\n"
)
assert ots_anchor in src
src = src.replace(ots_anchor, new_blocks + ots_anchor)

open('/home/z/my-project/tools/rescan54_12_fetch.py', 'w', encoding='utf-8').write(src)
print('written tools/rescan54_12_fetch.py,', len(src), 'bytes')
