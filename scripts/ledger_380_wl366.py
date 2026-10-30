#!/usr/bin/env python3
# ledger_380_wl366.py — ledger №380 + worklog 54-366 (pass#103, 06:02 UTC)
import hashlib, os

REPO = '/home/z/my-project'
LEDGER = os.path.join(REPO, 'output/08_monitoring/ledger.md')
WORKLOG = os.path.join(REPO, 'worklog.md')

res = hashlib.sha256(open(LEDGER, 'rb').read()).hexdigest()[:8]
assert res != '', 'empty ledger'

txt = open(LEDGER, encoding='utf-8').read()
last = [l for l in txt.splitlines() if l.strip().startswith('## Запись №')]
assert last and '№379' in last[-1], f'последний ledger: {last[-1:]!r}'

entry = """## Запись №380 — LONG30 pass#103 06:02→06:03 UTC — взрыв 197233 +20, stm-твинк 197255, гэпы стабильны
- sweep: 12 дельт-сигнатур (окно 268). ВЗРЫВ-МАГНИТ: 197233 «А че так много твинков? Селфдефенс?» +20 38→58 (ускорение: +11 за 30 мин → +20 за 30 мин; гэп стабилен 1 — вырез не трогают, тред жарит). STM-ТВИНК: NEW-THREAD 197255 «Мой глазик увидел алмазик» (05:59, 1/1) OP=stm:76561199237721446 — fake-стим-детект сработал, deep-заход 1 [197255] выполнен (верификация). 112917 «нереального вайба тред» +3 68060→68063; 187993 «Братство Пульса» +1 1318→1319 (гэп 7 стабилен); 197010 +1 75→76; 197098 «Награды за лиги» +3 303→306 (гэп 4); 197149 «Патчноут» +1 146→147 (гэп 5); 197205 «Арена» +1 30→31 (гэп 1); 197223 «Арена» +3 9→12; 197234 «Позор компашки exba…» +1 56→57; 197239 «Рекомендации по кастомизации профиля» +1 12→13; 197241 «Яромир,поздравь» +1 15→16 (гэп 1); 197251 «нойте» +4 9→13 (кросс s15 05:55 подтверждён, гэп 1).
- ГЭП-КАРТИНА: все вырезы стабильны (187993=7, 197098=4, 197149=5, 197205/233/241/251=1) — модерация не докручивает с 04:32; утро: волна фидбека ивента продолжается (197251-254 рождены с 04:44).
- EXT: 0 событий — официоз молчит ~13.1ч после «Компенсации» (17:00) — рекорд продолжает расти (форум: 12 дельт/30 мин + 4 young-треда; каналы: ноль). YT RSS 404 x10 (тех-варн). VK: без новых.
- deep: 1 [197255] (stm-верификация). OWW 259 (проверено 20, из них OWW-FAIL 197142/153 = VANISH).
- VANISH: 197142/197153 404×2 = 29-й раунд подряд. integrity: нет (проход 103 не 4-й; force_integrity=False — 4-й будет #104).
- кросс-линия: WIPE-69 ~05:55 (12-й, recovery 4 шага OK, уроки gitconfig/creds учтены, потери 0); s15 05:55 — 197251 +3, RECONCILE-ADD 197253 «Чуть чуть про арену» (05:41) + 197254 «Чё ты недоволен наградой да?» (05:47); s35 05:35 — new=0. young active=4.
- [SKIP]-маркеров нет (0).
- git: lite a61f1136 (05:55) → long30 pass#103.
"""
with open(LEDGER, 'a', encoding='utf-8') as f:
    f.write('\n' + entry)
txt2 = open(LEDGER, encoding='utf-8').read()
last2 = [l for l in txt2.splitlines() if l.strip().startswith('## Запись №')]
assert '№380' in last2[-1], 'ledger verify failed'

wl = open(WORKLOG, encoding='utf-8').read()
tail_ids = [l for l in wl.splitlines() if l.strip().startswith('Task ID: 54-')]
last_num = 0
for l in tail_ids:
    t = l.split('Task ID: 54-')[1].split(':')[0].strip()
    if t.isdigit():
        last_num = max(last_num, int(t))
assert last_num == 365, f'worklog last={last_num}, ожидался 365'

line = 'Task ID: 54-366: sweep 12 сигнатур (взрыв 197233 +20 38→58 магнит утра; NEW-THREAD 197255 stm-твинк stm:76561199237721446; 112917 +3; 197098/223/251 по +3-4; остальное по +1 — гэпы все стабильны), EXT 0 (официоз молчит ~13.1ч рекорд; YT RSS 404 x10), deep 1 [197255 stm-верификация], OWW 259 (проверено 20); VANISH 197142/153 404×2 = 29-й раунд; кросс-линия: WIPE-69 recovery + s15 197253/254 RECONCILE-ADD; [SKIP]-маркеров нет'
with open(WORKLOG, 'a', encoding='utf-8') as f:
    f.write('\n' + line + '\n')
wl2 = open(WORKLOG, encoding='utf-8').read()
assert 'Task ID: 54-366:' in wl2, 'worklog verify failed'

print('LEDGER №380 OK + WORKLOG 54-366 OK')
