#!/usr/bin/env python3
# fix54_214_final.py — ГИТ-ФИКСАЦИЯ в ledger + финал в worklog
LEDGER = '/home/z/my-project/output/08_monitoring/ledger.md'
WORKLOG = '/home/z/my-project/worklog.md'

git_line = "- ГИТ-ФИКСАЦИЯ №254: secret_guard clean → commit 8dd9e759 → dual push ЗЕЛЁНЫЙ 68cd73f9..8dd9e759 (ОБЕ репы, 05:3x UTC — creds восстановлены в начале раунда, push с первого раза); bundle 20261025_0537 (308МБ — ротация начата заново после вайпа /home/z/backups, старше 3 чистить)\n"

final_block = """
---
Task ID: 54-214 (финал)
Agent: main
Task: Фиксация итогов раунда

Work Log:
- (3) ledger №254 append + ГИТ-ФИКСАЦИЯ, worklog 54-214 + финал → round commit 8dd9e759 → dual push ЗЕЛЁНЫЙ 68cd73f9..8dd9e759 (ОБЕ репы, 05:3x UTC) → bundle 0537 (308МБ) → чистка (в ротации 1 — после вайпа)

Stage Summary:
- Финальный healthcheck: ожидание STATE HEALTHY (8dd9e759 = обеим репам, bundle 0537); раунд 54-214 закрыт PUSHED — WIPE-31 recovery + полный обход одним циклом, зелёный с первого push
"""

with open(LEDGER, 'a', encoding='utf-8') as f:
    f.write(git_line)
with open(WORKLOG, 'a', encoding='utf-8') as f:
    f.write(final_block)
print('ГИТ-ФИКСАЦИЯ + финал записаны')
