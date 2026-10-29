#!/usr/bin/env python3
# ledger_378_wl364.py — ledger №378 + worklog 54-364 (pass#101, 05:02 UTC)
import hashlib, os

REPO = '/home/z/my-project'
LEDGER = os.path.join(REPO, 'output/08_monitoring/ledger.md')
WORKLOG = os.path.join(REPO, 'worklog.md')

res = hashlib.sha256(open(LEDGER, 'rb').read()).hexdigest()[:8]
assert res == 'c91ff4c0', f'ledger sha mismatch: {res} (ожидание c91ff4c0)'

txt = open(LEDGER, encoding='utf-8').read()
last = [l for l in txt.splitlines() if l.strip().startswith('## Запись №')]
assert last and '№377' in last[-1], f'последний ledger: {last[-1:]!r}'

entry = """## Запись №378 — LONG30 pass#101 05:02→05:03 UTC — вырез 197233, утренний разгон 197195 продолжается
- sweep: 5 сигнатур (NEW-POSTS ×5). ВЫРЕЗ: 197233 «А че так много твинков? Селфдефенс?» +6 21→27, гэп 0→1 (вторая ночная правка подряд, после 197241). Разгон утреннего магнита: 197195 «А где праздник и награды?» +4 115→119 (пик ночи 14/ч → устойчивые ~4-6/ч). 197140 «Чего брать на талоны?» +4 18→22. 197236 «Фидбек ивента, который мы ждали 5 месяцев» +1 25→26. 197247 «чет мыльно после патча» +1 11→12.
- EXT: 0 событий — официоз молчит ~12.1ч после «Компенсации» (17:00) — новый абсолютный рекорд молчания на фоне живого форума (197251 новорождён, 197195 разгоняется). YT RSS 404 x8 (постоянный тех-варн). VK-статьи: те же 6 из очереди, без новых.
- deep: 0. OWW 255 (проверено 20, из них OWW-FAIL 197142/197153 = VANISH-контроль).
- VANISH: 197142/197153 404×2 = 27-й раунд подряд.
- integrity: не выполнялся (проход 101 — не 4-й; канон #48 + GG×4 — PASS на pass#100).
- кросс-линия: WIPE-67 ~04:55 (10-й вайп, recovery 4 шага, потери 0); s15 04:55 — 197250 «Агрессивный фидбек» GRADUATED (237; цикл 02:45→04:55, пик 14), RECONCILE-ADD 197251 (04:44, lpn/cc 5/4, гэп 1 с рождения — утренний ВЫРЕЗ-кандидат, подтвердить на следующих проходах).
- [SKIP]-маркеров нет (0).
- git: lite 13527290 (04:55) → long30 pass#101.
"""
with open(LEDGER, 'a', encoding='utf-8') as f:
    f.write('\n' + entry)
txt2 = open(LEDGER, encoding='utf-8').read()
last2 = [l for l in txt2.splitlines() if l.strip().startswith('## Запись №')]
assert '№378' in last2[-1], 'ledger verify failed'

wl = open(WORKLOG, encoding='utf-8').read()
tail_ids = [l for l in wl.splitlines() if l.strip().startswith('Task ID: 54-')]
last_num = 363
for l in tail_ids:
    t = l.split('Task ID: 54-')[1].split(':')[0].strip()
    if t.isdigit():
        last_num = max(last_num, int(t))
assert last_num == 363, f'worklog last={last_num}, ожидался 363'

line = 'Task ID: 54-364: sweep 5 сигнатур (NEW-POSTS ×5: вырез 197233 гэп 0→1 21→27; 197195 +4 115→119 разгон; 197140 +4 18→22; 197236/197247 по +1), EXT 0 (официоз молчит ~12.1ч рекорд; YT RSS 404 x8), deep 0, OWW 255 (проверено 20); VANISH 197142/153 404×2 = 27-й раунд; кросс-линия: WIPE-67 recovery + 197250 GRADUATED 237 + 197251 RECONCILE-ADD (5/4, гэп 1 с рождения); [SKIP]-маркеров нет'
with open(WORKLOG, 'a', encoding='utf-8') as f:
    f.write('\n' + line + '\n')
wl2 = open(WORKLOG, encoding='utf-8').read()
assert 'Task ID: 54-364:' in wl2, 'worklog verify failed'

print('LEDGER №378 OK + WORKLOG 54-364 OK')
