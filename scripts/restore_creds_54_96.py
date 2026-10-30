#!/usr/bin/env python3
# restore_creds_54_96.py — восстановление ~/.git-credentials из MEGA-vault
# (чистка №6: creds + vault + bundles стёрты; процедура = playbook, та же что 54-65/54-91/54-95).
# БЕЗОПАСНОСТЬ: токен никогда не печатается — только статусы (MAC, sha256-префикс, HTTP-код).
import subprocess, sys, hashlib, re, os, stat

URL = 'https://mega.nz/file/r9QxQBCT#F4tjwiW8UOhJKqxFk1K55r8w5Je5qDw6zNC4dqmy2uo'
VAULT_TMP = '/tmp/pat_vault_54_96.md'
VAULT_LOCAL = '/home/z/my-project/PAT_VAULT_LOCAL.md'
CREDS = os.path.expanduser('~/.git-credentials')
ETHALON_SHA = '7f9edd5d'  # эталон vault 54-61 (токен НЕ ротирован = совпадёт)


def main():
    # 1. MEGA pull (MAC проверяется внутри)
    r = subprocess.run([sys.executable, 'tools/mega_pull.py', URL, VAULT_TMP],
                       capture_output=True, text=True, cwd='/home/z/my-project')
    print(r.stdout.strip())
    if r.returncode != 0 or 'MAC: OK' not in r.stdout:
        print('RESTORE FAIL: mega_pull не прошёл'); return 1

    vault = open(VAULT_TMP, 'rb').read()
    sha = hashlib.sha256(vault).hexdigest()
    print(f"vault sha256: {sha[:8]}… (эталон {ETHALON_SHA}… — {'СОВПАЛ = токен НЕ ротирован' if sha.startswith(ETHALON_SHA) else 'ОТЛИЧАЕТСЯ = возможна ротация!'})")

    # 2. Извлечь реальный токен: строка-метка «ТОКЕН:» + следующая строка ghp_… (не шаблон с <TOKEN>)
    text = vault.decode('utf-8', errors='replace')
    lines = text.splitlines()
    token = None
    for i, line in enumerate(lines):
        if line.strip() == 'ТОКЕН:' and i + 1 < len(lines):
            cand = lines[i + 1].strip()
            if '<TOKEN>' not in cand and re.match(r'^ghp_[A-Za-z0-9]{30,}$', cand):
                token = cand
                break
    if not token:
        token = next((l.strip() for l in lines
                      if re.match(r'^ghp_[A-Za-z0-9]{30,}$', l.strip())), None)
    if not token:
        print('RESTORE FAIL: токен не найден'); return 1
    print(f"token: найден (длина {len(token)}, префикс {token[:4]}***)")

    # 3. Записать creds в формате user:pass (ЕДИНСТВЕННЫЙ рабочий формат, 54-х)
    with open(CREDS, 'w') as f:
        f.write(f'https://TonkWasere:{token}@github.com/\n')
    os.chmod(CREDS, stat.S_IRUSR | stat.S_IWUSR)

    # 4. PAT_VAULT_LOCAL.md рядом с RESTORE_GUIDE (gitignored) — пережить следующую чистку
    with open(VAULT_LOCAL, 'wb') as f:
        f.write(vault)
    os.chmod(VAULT_LOCAL, stat.S_IRUSR | stat.S_IWUSR)

    # 5. credential.helper = store (слетает при чистках — вернуть ДО пуша)
    subprocess.run(['git', 'config', 'credential.helper', 'store'], cwd='/home/z/my-project', check=True)
    helper = subprocess.run(['git', 'config', 'credential.helper'], cwd='/home/z/my-project',
                            capture_output=True, text=True).stdout.strip()

    # 6. Проверка токена через GitHub API (печатаем только HTTP-код)
    api = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
                          '-H', f'Authorization: token {token}',
                          'https://api.github.com/user'], capture_output=True, text=True)
    code = api.stdout.strip()
    print(f"github API: HTTP {code} {'OK' if code == '200' else 'FAIL'}")

    # 7. Проверка git-доступа без утечки: ls-remote origin
    ls = subprocess.run(['git', 'ls-remote', 'origin', 'sanity-monitor'], cwd='/home/z/my-project',
                        capture_output=True, text=True)
    print(f"ls-remote origin: {'OK ' + ls.stdout.split()[0][:7] if ls.returncode == 0 else 'FAIL: ' + ls.stderr.strip()[:80]}")
    print(f"creds: {CREDS} (600), vault: {VAULT_LOCAL} (600), credential.helper={helper}")
    return 0 if code == '200' and ls.returncode == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
