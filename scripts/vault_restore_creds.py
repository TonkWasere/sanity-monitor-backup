#!/usr/bin/env python3
# vault_restore_creds.py — восстановление ~/.git-credentials из /tmp/PAT_VAULT_LOCAL.md
# (рецепт чек-листа WIPE, страховка 54-209-B; токен НИКОГДА не печатается/не логируется)
import re, os, sys, subprocess

VAULT = '/tmp/PAT_VAULT_LOCAL.md'
t = open(VAULT, encoding='utf-8').read()
m = re.search(r'^ghp_[A-Za-z0-9_]+', t, re.M)
if not m:
    print('FAIL: строка ТОКЕН (ghp_) в vault не найдена'); sys.exit(1)
tok = m.group(0)

# 1) creds file (формат https://user:token@github.com), chmod 600
p = os.path.expanduser('~/.git-credentials')
with open(p, 'w') as f:
    f.write('https://TonkWasere:' + tok + '@github.com\n')
os.chmod(p, 0o600)
os.chmod(VAULT, 0o600)
print('CREDS-OK: ~/.git-credentials (600) восстановлен из vault')

# 2) helper=store (слетает при каждой чистке — возвращать ДО пуша)
r = subprocess.run(['git', 'config', '--global', 'credential.helper', 'store'],
                   capture_output=True, text=True)
print('HELPER-OK' if r.returncode == 0 else 'HELPER-FAIL: ' + r.stderr)

# 3) API verify: только HTTP-код + логин, сам токен не выводится
r = subprocess.run(['curl', '-s', '-H', 'Authorization: token ' + tok,
                    'https://api.github.com/user'],
                   capture_output=True, text=True)
try:
    import json
    j = json.loads(r.stdout)
    print('API VERIFY: HTTP-код полей login/id =', j.get('login'), '/', j.get('id'))
except Exception:
    print('API VERIFY FAIL:', r.stdout[:200])

# 4) backups dir
os.makedirs('/home/z/backups', exist_ok=True)
print('BACKUPS-DIR-OK: /home/z/backups создан/существует')
