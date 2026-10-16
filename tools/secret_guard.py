#!/usr/bin/env python3
# secret_guard.py — pre-commit guard: не даём закоммитить секрет (PAT и подобные).
# Появился после инцидента 15.10.2026 ~22:49 UTC (токен автора отозван GitHub'ом;
# наша git-история чиста — проверено git log -S по телу токена, но guard —
# страховка от ЛЮБОЙ случайной утечки в будущем).
# Никогда не печатает полное значение секрета — только файл:строка и замаскированный префикс.
# Использование:
#   python3 tools/secret_guard.py          # скан staged-диффа (перед КАЖДЫМ коммитом раунда)
#   python3 tools/secret_guard.py --head   # + скан всего рабочего дерева (трекнутые файлы)
import re, subprocess, sys

PATTERNS = [
    ('github_pat_fine_grained', re.compile(r'github_pat_[A-Za-z0-9_]{20,}')),
    ('ghp_classic_pat', re.compile(r'ghp_[A-Za-z0-9]{30,}')),
    ('gho_oauth', re.compile(r'gho_[A-Za-z0-9]{30,}')),
    ('ghu_user_token', re.compile(r'ghu_[A-Za-z0-9]{30,}')),
    ('ghs_server_token', re.compile(r'ghs_[A-Za-z0-9]{30,}')),
    ('cred_url_embedded_token', re.compile(r'https://[A-Za-z0-9_-]{30,}@github\.com')),
    ('cred_url_userpass_token', re.compile(r'https://[A-Za-z0-9_.-]+:[A-Za-z0-9_-]{30,}@github\.com')),
]

def scan(text, src):
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for name, rx in PATTERNS:
            m = rx.search(line)
            if m:
                v = m.group(0)
                masked = v[:8] + '...[' + str(len(v)) + ' chars masked]'
                hits.append(f'{src}:{lineno}: {name} -> {masked}')
    return hits

def main():
    hits = []
    # 1) staged diff (то, что реально уйдёт в коммит)
    diff = subprocess.run(['git', 'diff', '--cached', '-U0'], capture_output=True, text=True)
    if diff.returncode == 0 and diff.stdout:
        for line in diff.stdout.splitlines():
            if line.startswith('+') and not line.startswith('+++'):
                hits += scan(line[1:], 'staged-diff')
    # 2) опционально всё рабочее дерево (трекнутые файлы)
    if '--head' in sys.argv:
        ls = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
        for f in ls.stdout.splitlines():
            try:
                content = open(f, encoding='utf-8', errors='ignore').read()
            except Exception:
                continue
            hits += scan(content, f'worktree:{f}')
    if hits:
        print('!!! SECRET GUARD: ПОХОЖЕ НА СЕКРЕТ В КОММИТЕ — КОММИТ ПРЕРВАН')
        for h in hits[:20]:
            print('  ' + h)
        print('Убери секрет из staged-изменений (git restore --staged <file> + правка) и повтори.')
        sys.exit(1)
    print('SECRET GUARD: clean')

if __name__ == '__main__':
    main()
