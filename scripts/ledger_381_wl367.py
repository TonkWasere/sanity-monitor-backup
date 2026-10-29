#!/usr/bin/env python3
# ledger_381_wl367.py — ledger №381 + worklog 54-367 (pass#104 integrity, 06:32 UTC)
import hashlib, os

REPO = '/home/z/my-project'
LEDGER = os.path.join(REPO, 'output/08_monitoring/ledger.md')
WORKLOG = os.path.join(REPO, 'worklog.md')

res = hashlib.sha256(open(LEDGER, 'rb').read()).hexdigest()[:8]
assert res != '', 'empty ledger'

txt = open(LEDGER, encoding='utf-8').read()
last = [l for l in txt.splitlines() if l.strip().startswith('## Запись №')]
assert last and '№380' in last[-1], f'последний ledger: {last[-1:]!r}'

entry = """## Запись №381 — LONG30 pass#104 06:32→06:34 UTC — INTEGRITY PASS, взрыв 197233 +44 (гэп 1→3), вырез 197251 подтверждён
- INTEGRITY: ДА — канон #48 (196411) sha256 MATCH; GG-якоря живы: 195574#69, 195660#387, 159759#14590+14591 (все alive, hidden=None).
- sweep: 13 дельт-сигнатур (окно 268). ВЗРЫВ ВЕКА: 197233 «А че так много твинков? Селфдефенс?» +44 58→102 (ускорение третье подряд: +11 → +20 → +44 за 30 мин; cc 57→99; гэп 1→3 — модерация докручивает ПАРАЛЛЕЛЬНО взрыву: 2 поста вырезано за окно). MIX-SIG/ВЫРЕЗ: 197251 «Форумные пожалуйста нойте лучше и быстрее» lpn 13→14, cc=12 фикс, гэп 1→2 — ПОДТВЕРЖДЁН кросс-линией (s15 06:25 поймала то же; deep-заход 1 [197251]). 197254 «Чё ты недоволен наградой» +8 4→12 (спринт); 197218 «РКН добрался» +4 18→22; 197205 «Арена» +2 31→33 (гэп 1); 197234 +5 57→62; 197239 +2 13→15; 197236 +1; 197241 +1 (гэп 1); 197243 «Фидбек по новому ивенту „Празднество"» +1 11→12; 197253 +2 6→8; 197255 stm-твинк +3 1→4; 187993 «Братство Пульса» +1 (гэп 7).
- ГЭП-КАРТИНА: докрутки вернулись — 197233 1→3 (2 выреза за окно при +44), 197251 1→2; старые стабильны (187993=7, 197098=4, 197149=5). Модерация активно чистит утреннюю волну фидбека.
- EXT: 0 событий — официоз молчит ~13.5ч после «Компенсации» (17:00) — рекорд растёт; форум в это же окно: +150 постов по 13 тредам. YT RSS 404 x11. VK: без новых.
- deep: 1 [197251] (верификация выреза). OWW 259 (проверено 20; OWW-FAIL 197142/153 = VANISH).
- VANISH: 197142/197153 404×2 = 30-й раунд подряд.
- кросс-линия: WIPE-70 ~06:25 (13-й, recovery 4 шага OK, потери 0); s15 06:25 — ВЫРЕЗ 197251 гэп 1→2 (сработала раньше свипа на 7 мин), 197254 +5, 197253 +2, RECONCILE-ADD 197255; young active=5.
- [SKIP]-маркеров нет (0).
- git: lite 8149a5b3 (06:25) → long30 pass#104.
"""
with open(LEDGER, 'a', encoding='utf-8') as f:
    f.write('\n' + entry)
txt2 = open(LEDGER, encoding='utf-8').read()
last2 = [l for l in txt2.splitlines() if l.strip().startswith('## Запись №')]
assert '№381' in last2[-1], 'ledger verify failed'

wl = open(WORKLOG, encoding='utf-8').read()
tail_ids = [l for l in wl.splitlines() if l.strip().startswith('Task ID: 54-')]
last_num = 0
for l in tail_ids:
    t = l.split('Task ID: 54-')[1].split(':')[0].strip()
    if t.isdigit():
        last_num = max(last_num, int(t))
assert last_num == 366, f'worklog last={last_num}, ожидался 366'

line = 'Task ID: 54-367: sweep INTEGRITY PASS (канон #48 MATCH, GG×4 живы), 13 сигнатур (взрыв 197233 +44 58→102 гэп 1→3 — модерация докручивает параллельно; MIX-SIG вырез 197251 гэп 1→2 кросс подтверждён; 197254 +8; 197218 +4), EXT 0 (официоз молчит ~13.5ч рекорд; YT RSS 404 x11), deep 1 [197251], OWW 259 (проверено 20); VANISH 197142/153 404×2 = 30-й раунд; кросс-линия: WIPE-70 recovery + s15 ВЫРЕЗ 197251; [SKIP]-маркеров нет'
with open(WORKLOG, 'a', encoding='utf-8') as f:
    f.write('\n' + line + '\n')
wl2 = open(WORKLOG, encoding='utf-8').read()
assert 'Task ID: 54-367:' in wl2, 'worklog verify failed'

print('LEDGER №381 OK + WORKLOG 54-367 OK')
