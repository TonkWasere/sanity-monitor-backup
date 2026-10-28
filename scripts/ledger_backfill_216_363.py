# -*- coding: utf-8 -*-
# Backfill ledger: реконструкция сожжённого поколения №216-363 из worklog-строк 54-<NNN>.
# Вставка перед "## Запись №364–366 [REBUILD-WIPE58]". Нумерация зажата до №363.
import re, subprocess

LEDGER = '/home/z/my-project/output/08_monitoring/ledger.md'
CAP_NO = 363          # №364 занят [REBUILD]-записью
FIRST_NO = 216        # файл обрывался на №215
MAXLEN = 700          # трим содержимого на запись

ledger = open(LEDGER, encoding='utf-8').read()

# 1) граница: последний (Task 54-<NNN> в существующих записях (эра до [REBUILD])
head = ledger.split('## Запись №364–366 [REBUILD-WIPE58]')[0]
boundary_tasks = [int(m) for m in re.findall(r'\(Task 54-(\d+)', head)]
boundary = max(boundary_tasks) if boundary_tasks else 0
print('boundary Task ID: 54-%d (последняя запись в ledger: №%s)' % (
    boundary, re.findall(r'№(\d+)', head)[-1]))

# 2) корпус: числовые worklog-строки 54-<NNN> с NNN > boundary
wl = open('/home/z/my-project/worklog.md', encoding='utf-8').read().splitlines()
corpus = []
for line in wl:
    m = re.match(r'Task ID: 54-(\d+): (.+)$', line)
    if m and int(m.group(1)) > boundary:
        corpus.append((int(m.group(1)), m.group(2).strip()))
corpus.sort()
print('corpus: %d worklog-строк (54-%d..54-%d)' % (
    len(corpus), corpus[0][0] if corpus else 0, corpus[-1][0] if corpus else 0))

# 3) генерация записей; если строк больше, чем номеров до CAP_NO — хвост вливаем в последнюю
nos = list(range(FIRST_NO, CAP_NO + 1))
entries = []
overflow = max(0, len(corpus) - len(nos))
for i, (nnn, content) in enumerate(corpus):
    if i < len(nos):
        no = nos[i]
    else:
        no = nos[-1]  # вливаем в последнюю
    body = content if len(content) <= MAXLEN else content[:MAXLEN - 3] + '...'
    tag = '' if i < len(nos) else ' (+перелив из след. раундов)'
    entries.append(
        '## Запись №%d [RECONSTRUCTED-FROM-WORKLOG] — %s\n'
        '(источник: worklog 54-%d; полный ledger-текст записи утрачен в WIPE-56/58, '
        'реконструкция 29.10 ~00:00 UTC, job 481043)%s\n' % (no, body, nnn, tag))

block = ('\n<!-- BACKFILL: реконструкция №%d-№%d из worklog; канонические тексты утрачены '
         'в WIPE-58, возможны лакуны (пропуски проходов не писали worklog-строк) -->\n%s'
         % (FIRST_NO, min(CAP_NO, FIRST_NO + len(corpus) - 1), '\n'.join(entries)))

# 4) вставка перед [REBUILD]-записью №364-366
anchor = '## Запись №364–366 [REBUILD-WIPE58]'
idx = ledger.find(anchor)
assert idx > 0, 'anchor not found'
ledger_new = ledger[:idx] + block + '\n' + ledger[idx:]
open(LEDGER, 'w', encoding='utf-8').write(ledger_new)

cnt = len(re.findall(r'^## Запись', ledger_new, re.M))
print('записей всего в файле: %d; вставлено: %d; перелив: %d' % (cnt, len(entries), overflow))
print('OK backfill')
