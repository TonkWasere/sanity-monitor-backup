#!/usr/bin/env python3
# creds_from_vault.py — восстановление ~/.git-credentials из /tmp/PAT_VAULT_LOCAL.md
# БЕЗ печати секрета: выводит только статус/длины/HTTP-код.
import os, re, sys, json, urllib.request, hashlib

VAULT = '/tmp/PAT_VAULT_LOCAL.md'
CREDS = os.path.expanduser('~/.git-credentials')
USER = 'TonkWasere'

text = open(VAULT, encoding='utf-8', errors='replace').read()

# Ищем токен: классик ghp_ (36) или fine-grained github_pat_
tok = None
m = re.search(r'ghp_[A-Za-z0-9]{36,40}', text)
if m:
    tok = m.group(0)
else:
    m = re.search(r'github_pat_[A-Za-z0-9_]{60,90}', text)
    if m:
        tok = m.group(0)
if not tok:
    print('ERR: token pattern not found in vault')
    sys.exit(2)

# user:pass строка для credential-helper store
line = f'https://{USER}:{tok}@github.com'
with open(CREDS, 'w', encoding='utf-8') as f:
    f.write(line + '\n')
os.chmod(CREDS, 0o600)

print(f'creds written: {CREDS} ({os.path.getsize(CREDS)}B, mode 600, sha256_8={hashlib.sha256(line.encode()).hexdigest()[:8]})')

# Verify: API 200 (логин TonkWasere)
req = urllib.request.Request('https://api.github.com/user', headers={
    'Authorization': f'token {tok}',
    'User-Agent': 'monitoring-recovery',
})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.loads(r.read().decode())
        print(f'API: HTTP {r.status}, login={body.get("login")}')
except Exception as e:
    print(f'API verify FAILED: {type(e).__name__} {e}')
    sys.exit(3)
print('OK')
