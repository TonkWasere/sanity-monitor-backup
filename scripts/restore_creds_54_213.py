#!/usr/bin/env python3
# restore_creds_54_213.py — восстановление ~/.git-credentials из MEGA-vault
# (WIPE-30, шаг 2 чек-листа). Токен НИКОГДА не печатается и не попадает
# в bash-переменные — только внутри этого процесса.
import re, os, json, urllib.request, hashlib

VAULT = '/tmp/PAT_VAULT_LOCAL.md'
CREDS = os.path.expanduser('~/.git-credentials')

v = open(VAULT, encoding='utf-8', errors='replace').read()
print('vault sha256:', hashlib.sha256(v.encode()).hexdigest()[:8], '(эталон 7f9edd5d)')
m = re.search(r'ТОКЕН:\s*(\S+)', v)
assert m, 'line ТОКЕН not found'
tok = m.group(1)
assert tok != '<TOKEN>' and len(tok) > 20, 'template/stub line!'

with open(CREDS, 'w') as f:
    f.write(f'https://TonkWasere:{tok}@github.com/\n')
os.chmod(CREDS, 0o600)
print(f'creds written (600), token_len={len(tok)}')

req = urllib.request.Request('https://api.github.com/user', headers={'Authorization': f'token {tok}', 'User-Agent': 'sanity-monitor'})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        code = r.status
except Exception as e:
    code = getattr(e, 'code', str(e))
print('API user:', code)
req2 = urllib.request.Request('https://api.github.com/repos/TonkWasere/test', headers={'Authorization': f'token {tok}', 'User-Agent': 'sanity-monitor'})
try:
    with urllib.request.urlopen(req2, timeout=20) as r:
        code2 = r.status
except Exception as e:
    code2 = getattr(e, 'code', str(e))
print('API repo:', code2)
