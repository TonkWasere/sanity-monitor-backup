#!/usr/bin/env python3
# ledger_383_wl369.py — ledger №383 + worklog 54-369 (pass#106, 07:32 UTC; MEGA 509)
import hashlib, os

REPO = '/home/z/my-project'
LEDGER = os.path.join(REPO, 'output/08_monitoring/ledger.md')
WORKLOG = os.path.join(REPO, 'worklog.md')

res = hashlib.sha256(open(LEDGER, 'rb').read()).hexdigest()[:8]
assert res != '', 'empty ledger'

txt = open(LEDGER, encoding='utf-8').read()
last = [l for l in txt.splitlines() if l.strip().startswith('## Запись №')]
assert last and '№382' in last[-1], f'последний ledger: {last[-1:]!r}'

entry = """## Запись №383 — LONG30 pass#106 07:32→07:34 UTC — второй stm-твинк 197258, взрыв 197233 замедлился (+10), 197234 VANISH-подозрение 2-й раунд
- sweep: 11 дельт-сигнатур (окно 268). STM-ТВИНК ×2 ЗА УТРО: NEW-THREAD 197258 «Идея для добавление в ивент нового оружие для разнообразия» (07:28, 1/1) OP=stm:76561198069432276 — второй fake-стим после 197255 (05:59); deep-заход 1 [197258] верификация выполнена. ВЗРЫВ-ЗАМЕДЛЕНИЕ: 197233 «А че так много твинков?» +10 128→138 (после +44/+26; гэп стабилен 4 — модерация прекратила докрутку этого треда). 197254 «недоволен наградой» +4 18→22 (кросс s15); 197256 «Скидки на бартер» +4 3→7 (кросс s15); 197236 +3 32→35; 112917 +2 68064→68066; 114800 «Неофициальный нарративный щитпостинг» +1 12951→12952 (гэп 124 стабилен); 179857 «Курилка арт-отдела» +1 (OWW); 197188 «ваш профиль» +1 65→66; 197207 +1 90→91; 197239 +1 17→18; 197241 +1 17→18 (гэп 1).
- ВАНИШ-ПОДОЗРЕНИЕ: OWW-FAIL [197234] «Позор компашки exba....» 2-й раунд подряд (после pass#105 57→62): два последовательных неудачи целевого GET — вероятно 404 (снесён модерацией?) либо стойкий сетевой транзиент. Статус: не подтверждён deep'ом (deep ушёл на stm-верификацию 197258); контроль на pass#107.
- EXT: 3 события — VK FP-осцилляция ПОДТВЕРЖДЕНА: заглушка fp cbe5cfdf7c21 (записана 07:05) вернулась к оригинальным fp (cep-raspada 892a8608, patchnout-2810 a5743d17, otkrytie-testovogo 9318c249) — «ИЗМЕНЕНА» ложные (mod-даты старые); VK отдаёт нестабильный рендер. Контентных изменений НЕТ. YT RSS: OK второй прогон подряд. ТГК stalzone молчит ~14.7ч (рекорд растёт; last_id=3256 «Компенсация» 28.10 17:00). Steam: без изменений.
- deep: 1 [197258 stm]. OWW 262 (проверено 21; OWW-FAIL 197142/153 = VANISH 32-й раунд; OWW-FAIL 197234 = подозрение 2-й раунд).
- VANISH: 197142/197153 404×2 = 32-й раунд подряд.
- integrity: нет (проход 106 не 4-й; PASS был #104).
- ИНФРА: WIPE-72 ~07:25 (15-й) recovery частично — MEGA 509 повторно (vault/creds недоступны); push pending: lite 07:25 + этот ledger локальны. MEGA-цикл: 509 на 06:55 → отпустил 07:10 → 509 на 07:25. Данные локальны, потери 0.
- кросс-линия: s15 07:25 — 197252 GRADUATED (239), 197254 +4, 197256 +3, RECONCILE-ADD 197257 «Страшная очень страшна!1!11!» (07:20, 3/3); s15 07:10 — MEGA recovered, push дожат, 197255 +1 stm, 197256 +2. young active=5.
- [SKIP]-маркеров нет (0).
- git: lite 87b37f26 (07:25, push pending) → long30 pass#106 (push pending).
"""
with open(LEDGER, 'a', encoding='utf-8') as f:
    f.write('\n' + entry)
txt2 = open(LEDGER, encoding='utf-8').read()
last2 = [l for l in txt2.splitlines() if l.strip().startswith('## Запись №')]
assert '№383' in last2[-1], 'ledger verify failed'

wl = open(WORKLOG, encoding='utf-8').read()
tail_ids = [l for l in wl.splitlines() if l.strip().startswith('Task ID: 54-')]
last_num = 0
for l in tail_ids:
    t = l.split('Task ID: 54-')[1].split(':')[0].strip()
    if t.isdigit():
        last_num = max(last_num, int(t))
assert last_num == 368, f'worklog last={last_num}, ожидался 368'

line = 'Task ID: 54-369: sweep 11 сигнатур (NEW-THREAD 197258 stm-твинк второй за утро stm:76561198069432276; 197233 замедлился +10 138 гэп 4; 197254/256 кросс +4; 197236 +3; OWW-FAIL 197234 «Позор компашки» VANISH-подозрение 2-й раунд — контроль на #107), EXT 3 (VK FP-осцилляция подтверждена — ложные ИЗМЕНЕНА; ТГК официоз молчит ~14.7ч рекорд; YT RSS OK), deep 1 [197258 stm-вериф], OWW 262 (проверено 21); VANISH 197142/153 404×2 = 32-й раунд; ИНФРА: WIPE-72 + MEGA 509 повторно — push pending; кросс-линия: s15 197252 GRADUATED 239 + 197257 RECONCILE-ADD; [SKIP]-маркеров нет'
with open(WORKLOG, 'a', encoding='utf-8') as f:
    f.write('\n' + line + '\n')
wl2 = open(WORKLOG, encoding='utf-8').read()
assert 'Task ID: 54-369:' in wl2, 'worklog verify failed'

print('LEDGER №383 OK + WORKLOG 54-369 OK')
