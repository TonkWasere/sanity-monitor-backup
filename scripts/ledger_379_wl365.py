#!/usr/bin/env python3
# ledger_379_wl365.py — ledger №379 + worklog 54-365 (pass#102, 05:32 UTC)
import hashlib, os

REPO = '/home/z/my-project'
LEDGER = os.path.join(REPO, 'output/08_monitoring/ledger.md')
WORKLOG = os.path.join(REPO, 'worklog.md')

res = hashlib.sha256(open(LEDGER, 'rb').read()).hexdigest()[:8]
assert res != '', 'empty ledger'

txt = open(LEDGER, encoding='utf-8').read()
last = [l for l in txt.splitlines() if l.strip().startswith('## Запись №')]
assert last and '№378' in last[-1], f'последний ledger: {last[-1:]!r}'

entry = """## Запись №379 — LONG30 pass#102 05:32→05:33 UTC — 13 дельт: взрыв 197233 +11, РКН-тема, гэпы стабильны
- sweep: 13 дельт-сигнатур. ВЗРЫВ: 197233 «А че так много твинков? Селфдефенс?» +11 27→38 (самый быстрый рост утра, магнит после вчерашнего выреза; гэп стабилен 1 — модерация не докручивает). НОВАЯ ТЕМА: 197218 «РКН добрался до stalzone» +1 17→18 — внешний регуляторный флэшмоб-кандидат. 112917 (гигант) +2 68058→68060 — за хвостом tail, по дифу 335→336. 197010 «Регистрация урона…» +4 71→75; 197098 «Награды за лиги» +4 299→303 (гэп 4 стабилен); 197149 «Патчноут» +2 144→146 (гэп 5 стабилен); 197140 +2 22→24; 197236 +2 26→28; 197195 +1 119→120 (утренний магнит замедлился после разгона 14/ч); 197205 «Арена» +1 29→30 (гэп 1); 197241 +1 14→15 (гэп 1); 197251 «нойте» +4 5→9 (гэп 1, кросс s15 подтверждён); NEW 197252 «Фидбек по празднеству» 1/1 (кросс s15 RECONCILE-ADD 05:21 подтверждён окном).
- ГЭП-КАРТИНА: все существующие вырезы стабильны (197098=4, 197149=5, 197205/233/241/251=1) — модерация не докручивает с 04:32; ночные правки закрыты, форум жарит по ивент-темам.
- EXT: 0 событий — официоз молчит ~12.5ч после «Компенсации» (17:00) — рекорд продолжает расти при живом форуме. YT RSS 404 x9 (постоянный тех-варн). VK: те же статьи, без новых.
- deep: 0. OWW 255 (проверено 20). VANISH: 197142/197153 404×2 = 28-й раунд подряд. integrity: нет (проход 102 не 4-й; force_integrity=False).
- кросс-линия: WIPE-68 ~05:25 (11-й, recovery 4 шага OK, mega_pull retry 1x, gitconfig сбит вайпом — credential.helper восстановлен; потери 0); s15 05:25 — 197251 +3, RECONCILE-ADD 197252; s15 05:10 — 197251 +1.
- [SKIP]-маркеров нет (0).
- git: lite 49fc2cfd (05:25) → long30 pass#102.
"""
with open(LEDGER, 'a', encoding='utf-8') as f:
    f.write('\n' + entry)
txt2 = open(LEDGER, encoding='utf-8').read()
last2 = [l for l in txt2.splitlines() if l.strip().startswith('## Запись №')]
assert '№379' in last2[-1], 'ledger verify failed'

wl = open(WORKLOG, encoding='utf-8').read()
tail_ids = [l for l in wl.splitlines() if l.strip().startswith('Task ID: 54-')]
last_num = 0
for l in tail_ids:
    t = l.split('Task ID: 54-')[1].split(':')[0].strip()
    if t.isdigit():
        last_num = max(last_num, int(t))
assert last_num == 364, f'worklog last={last_num}, ожидался 364'

line = 'Task ID: 54-365: sweep 13 дельт (NEW-POSTS ×12: взрыв 197233 +11 27→38 магнит; РКН-тема 197218; 197010/098 по +4; 112917 гигант +2; 197140/149/236 по +2; 197195/205/218/241/251 по +1 — гэпы все стабильны; NEW 197252 1/1), EXT 0 (официоз молчит ~12.5ч рекорд; YT RSS 404 x9), deep 0, OWW 255 (проверено 20); VANISH 197142/153 404×2 = 28-й раунд; кросс-линия: WIPE-68 recovery + s15 197252 RECONCILE-ADD подтверждён; [SKIP]-маркеров нет'
with open(WORKLOG, 'a', encoding='utf-8') as f:
    f.write('\n' + line + '\n')
wl2 = open(WORKLOG, encoding='utf-8').read()
assert 'Task ID: 54-365:' in wl2, 'worklog verify failed'

print('LEDGER №379 OK + WORKLOG 54-365 OK')
