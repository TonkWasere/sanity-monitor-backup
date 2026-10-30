#!/usr/bin/env python3
"""mega_fetch.py — восстановление PAT-vault с MEGA после вайпа ВМ.
Паттерн «подтянуть ссылку на Мегу из файла в Гите» (теория автора 54-209-B:
линк в теле репо — текст, не секрет; PAT в файле ССЫЛКИ, не здесь).

ИСТОЧНИКИ ССЫЛКИ (приоритет):
  1) argv[1] — разовая ручная ротация (автор прислал в чат)
  2) MEGA_VAULT_LINK_LOCAL.txt — gitignored, локальная ротация без коммита
  3) MEGA_VAULT_INSURANCE.md строка MEGA_LINK: — в гите (страховка от вайпов)
  4) HARD_LINK ниже — обновлять при КАЖДОЙ ротации вместе с INSURANCE

Урок 27.10.2026: движок pip-mega+tenacity снесён вайпом ВМ — используем
tools/mega_pull.py (stdlib, самодостаточный). Урок 15.10: формат creds
СТРОГО https://TonkWasere:<TOKEN>@github.com/ (user:pass, chmod 600).

Использование: python3 tools/mega_fetch.py [url]   → /tmp/mega_restore/
Дальше: см. PAT_VAULT_LOCAL.md внутри (gitignored-копия в корне репо).
"""
import os, re, subprocess, sys

# Ротация 27.10.2026 (~13:50 UTC, creds умерли 26.10, старый n5QmRLaJ мёртв)
HARD_LINK = "https://mega.nz/file/r9QxQBCT#F4tjwiW8UOhJKqxFk1K55r8w5Je5qDw6zNC4dqmy2uo"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def resolve():
    if len(sys.argv) > 1 and sys.argv[1].startswith('http'):
        return sys.argv[1], 'argv'
    p_local = os.path.join(ROOT, 'MEGA_VAULT_LINK_LOCAL.txt')
    if os.path.exists(p_local):
        for line in open(p_local, encoding='utf-8', errors='ignore'):
            if 'mega.nz/' in line:
                return line.strip(), 'LOCAL.txt'
    p_ins = os.path.join(ROOT, 'MEGA_VAULT_INSURANCE.md')
    if os.path.exists(p_ins):
        m = re.search(r'MEGA_LINK:\s*(\S+)', open(p_ins, encoding='utf-8', errors='ignore').read())
        if m:
            return m.group(1), 'INSURANCE'
    return HARD_LINK, 'hard'

url, src = resolve()
print('mega_fetch: link source =', src)
dest = '/tmp/mega_restore'
os.makedirs(dest, exist_ok=True)
pull = os.path.join(ROOT, 'tools', 'mega_pull.py')
r = subprocess.run([sys.executable, pull, url, os.path.join(dest, 'PAT_VAULT_LOCAL.md')],
                   capture_output=True, text=True)
print((r.stdout or '')[-800:])
if r.stderr:
    print('STDERR:', r.stderr[-400:])
sys.exit(r.returncode)
