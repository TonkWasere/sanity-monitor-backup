#!/usr/bin/env python3
# ledger_382_wl368.py — ledger №382 + worklog 54-368 (pass#105, 07:02 UTC; MEGA 509 push pending)
import hashlib, os

REPO = '/home/z/my-project'
LEDGER = os.path.join(REPO, 'output/08_monitoring/ledger.md')
WORKLOG = os.path.join(REPO, 'worklog.md')

res = hashlib.sha256(open(LEDGER, 'rb').read()).hexdigest()[:8]
assert res != '', 'empty ledger'

txt = open(LEDGER, encoding='utf-8').read()
last = [l for l in txt.splitlines() if l.strip().startswith('## Запись №')]
assert last and '№381' in last[-1], f'последний ledger: {last[-1:]!r}'

entry = """## Запись №382 — LONG30 pass#105 07:02→07:04 UTC — 197233 +26 (гэп 3→4), OWW-FAIL 197234 VANISH-кандидат, MEGA 509 push pending
- sweep: 10 дельт-сигнатур (окно 268). ВЗРЫВ-МАГНИТ продолжается: 197233 «А че так много твинков? Селфдефенс?» +26 102→128 (cc 99→124; гэп 3→4 — модерация докручивает каждое окно при взрыве; ускорение: +11 → +20 → +44 → +26). 197254 «Чё ты недоволен наградой» +6 12→18 (кросс s15; спринт затухает). 197205 «Арена» +3 33→36; 197236 +3 29→32; 197239 +2 15→17; 179857 «Курилка арт-отдела» +2 1663→1665 (OWW); 112917 +1 68063→68064; 197207 «Ивент провоцирует зависть» +1 89→90; 197218 «РКН» +1 22→23; 197255 stm-твинк +1 4→5.
- ВНИМАНИЕ: OWW-FAIL [197234] «Позор компашки exba…» — целевой GET впервые не удался (после 57→62 в pass#104): либо транзиент, либо ВАНИШ-кандидат — контроль на pass#106 (404 повторится → VANISH-статус).
- EXT: 2 события — VK FP-дрейф 2 статей (patchnout-2810 fp a5743d→cbe5cfdf, otkrytie-testovogo fp 9318c2→cbe5cfdf): нестабильный VK-рендер (одинаковый fp у разных статей = заглушка), НЕ контентные изменения. Урок: контрольный повторный прогон ext_sources перезаписал state (события первого прогона восстановлены аналитически) — больше не повторять. YT RSS ВОССТАНОВЛЕН после 404 x11 (0703.xml OK 32KB, диф vs seen пуст — новых видео нет). ТГК stalzone last_id=3256 («Компенсация» 28.10 17:00) — ОФИЦИОЗ МОЛЧИТ ~14.1ч — рекорд. spectrum_zone last_id=8087 (15:59). Steam: без изменений.
- deep: 0. OWW 260 (проверено 21; OWW-FAIL 197142/153 = VANISH 31-й раунд; OWW-FAIL 197234 = кандидат).
- VANISH: 197142/197153 404×2 = 31-й раунд подряд.
- integrity: нет (проход 105 не 4-й; INTEGRITY PASS был #104 — канон #48 MATCH, GG×4 живы).
- КРИТИЧНО-ИНФРА: WIPE-71 ~06:55 (14-й) recovery частично — MEGA HTTP 509 Bandwidth Limit Exceeded (лимит после 14 recovery за ночь): vault/creds недоступны, lite-коммит 18f29433 (06:55) и этот ledger — push pending. Данные локальны (git-every-pass), потери 0. MEGA отпустит лимит ~07:20-07:55.
- кросс-линия: s15 06:55 — 197251 GRADUATED (238, гэп 2 при выпуске), 197254 +4, RECONCILE-ADD 197256 «Скидки на бартер» (06:50); s35 06:35 new=0. young active=5.
- [SKIP]-маркеров нет (0).
- git: lite 18f29433 (06:55, push pending) → long30 pass#105 (push pending).
"""
with open(LEDGER, 'a', encoding='utf-8') as f:
    f.write('\n' + entry)
txt2 = open(LEDGER, encoding='utf-8').read()
last2 = [l for l in txt2.splitlines() if l.strip().startswith('## Запись №')]
assert '№382' in last2[-1], 'ledger verify failed'

wl = open(WORKLOG, encoding='utf-8').read()
tail_ids = [l for l in wl.splitlines() if l.strip().startswith('Task ID: 54-')]
last_num = 0
for l in tail_ids:
    t = l.split('Task ID: 54-')[1].split(':')[0].strip()
    if t.isdigit():
        last_num = max(last_num, int(t))
assert last_num == 367, f'worklog last={last_num}, ожидался 367'

line = 'Task ID: 54-368: sweep 10 сигнатур (взрыв 197233 +26 102→128 гэп 3→4; 197254 +6; 197205/236 по +3; OWW-FAIL 197234 «Позор компашки» VANISH-кандидат — контроль на #106), EXT 2 (VK FP-дрейф заглушки — не контент; YT RSS восстановлен после 404 x11, новых видео нет; ТГК официоз молчит ~14.1ч рекорд), deep 0, OWW 260 (проверено 21); VANISH 197142/153 404×2 = 31-й раунд; ИНФРА: WIPE-71 + MEGA 509 — vault/creds недоступны, push pending (18f29433 локален, потери 0); кросс-линия: s15 197251 GRADUATED 238 + RECONCILE-ADD 197256; [SKIP]-маркеров нет'
with open(WORKLOG, 'a', encoding='utf-8') as f:
    f.write('\n' + line + '\n')
wl2 = open(WORKLOG, encoding='utf-8').read()
assert 'Task ID: 54-368:' in wl2, 'worklog verify failed'

print('LEDGER №382 OK + WORKLOG 54-368 OK')
