#!/usr/bin/env python3
# state_healthcheck.py — Task 54-hc: проверка состояния мониторинга + авторекавери с GitHub.
# Запуск: python3 tools/state_healthcheck.py          → check (exit 0 = здоров, 1 = провал)
#         python3 tools/state_healthcheck.py --recover → check, при провале файлов/репо — recovery с origin
# НИКОГДА не печатает содержимое ~/.git-credentials.
import os, sys, subprocess, datetime, urllib.request

PROJ = '/home/z/my-project'
KEY_FILES = [
    'worklog.md',
    'output/08_monitoring/ledger.md',
    'output/08_monitoring/GIT_AUTOMATION.md',
]
KEY_DIRS = ['tools', 'output/evidence_post']
ORIGIN_URL = 'https://github.com/TonkWasere/test.git'
BRANCH = 'sanity-monitor'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}

def sh(cmd, cwd=PROJ, timeout=60):
    try:
        r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:
        return 1, str(e)

now = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
problems = []
recover_needed = False

print(f'=== STATE HEALTHCHECK @ {now} ===')

# A. Ключевые файлы
for f in KEY_FILES:
    p = os.path.join(PROJ, f)
    ok = os.path.isfile(p) and os.path.getsize(p) > 100
    print(f"  [{'OK' if ok else 'DEAD'}] {f}" + (f" ({os.path.getsize(p)}B)" if os.path.isfile(p) else ''))
    if not ok:
        problems.append(f'file dead: {f}')
        recover_needed = True
for d in KEY_DIRS:
    p = os.path.join(PROJ, d)
    n = len(os.listdir(p)) if os.path.isdir(p) else -1
    ok = n > 0
    print(f"  [{'OK' if ok else 'DEAD'}] {d}/ ({n} files)")
    if not ok:
        problems.append(f'dir dead: {d}')
        recover_needed = True

# B. Git-репо
rc, out = sh('git fsck --no-dangling 2>&1 | head -3')
git_ok = rc == 0
rc2, branch = sh('git branch --show-current')
branch = branch.strip()
branch_ok = branch == BRANCH
print(f"  [{'OK' if git_ok else 'DEAD'}] git fsck")
print(f"  [{'OK' if branch_ok else 'DEAD'}] branch = {branch or '(none)'}")
if not git_ok:
    problems.append('git fsck FAILED')
    recover_needed = True
if not branch_ok:
    problems.append(f'branch != {BRANCH}')
    recover_needed = True

# C. Credentials (без чтения содержимого)
cred = os.path.expanduser('~/.git-credentials')
cred_ok = os.path.isfile(cred) and oct(os.stat(cred).st_mode & 0o777) == '0o600'
print(f"  [{'OK' if cred_ok else 'DEAD'}] ~/.git-credentials (600)")
if not cred_ok:
    problems.append('credentials missing/perm — push будет 401, нужен токен от автора')

# D. Remote-синхронизация (ls-remote, не жрёт API rate limit; оба remote)
rc, head_local = sh('git rev-parse --short=12 HEAD')
head_local = head_local.strip()[:12]
for remote in ('origin', 'backup'):
    try:
        rc, out = sh(f'git ls-remote {remote} refs/heads/{BRANCH}', timeout=30)
        head_remote = out.strip().split('	')[0][:12] if rc == 0 and out.strip() else ''
        if rc != 0 or not head_remote:
            print(f'  [SKIP] {remote} unreachable: {out[:80]}')
        else:
            ok = head_remote == head_local
            print(f"  [{'OK' if ok else 'DRIFT'}] {remote}: local={head_local} remote={head_remote}")
            if not ok:
                problems.append(f'{remote} drift (push не доехал?)')
    except Exception as e:
        print(f'  [SKIP] {remote}: {e}')

# E. Дрейф последней активности (гэп кронинга) — по последнему коммиту
try:
    from datetime import timezone
    rc, out = sh("git log -1 --format=%cI", timeout=15)
    if rc == 0 and out.strip():
        last_dt = datetime.datetime.fromisoformat(out.strip().strip('Z').split('.')[0] + '+00:00' if not out.strip().endswith(('+00:00', 'Z')) else out.strip().replace('Z', '+00:00'))
        gap_h = (datetime.datetime.now(timezone.utc) - last_dt).total_seconds() / 3600
        print(f"  [{'OK' if gap_h < 3 else 'GAP'}] последний коммит: {gap_h:.1f} ч назад")
        if gap_h >= 3:
            problems.append(f'croning gap {gap_h:.1f}h — возможно cron/ВМ ушёл погулять (продолжить раунд, дельты за гэп покрыть одним резюме)')
except Exception as e:
    print(f'  [SKIP] gap check: {e}')

# F. Локальный bundle (третья линия)
import glob as _glob
bundles = sorted(_glob.glob('/home/z/backups/sanity-monitor-*.bundle'))
if bundles:
    age_h = (datetime.datetime.now(timezone.utc) - datetime.datetime.fromtimestamp(os.path.getmtime(bundles[-1]), timezone.utc)).total_seconds() / 3600
    print(f"  [{'OK' if age_h < 26 else 'STALE'}] bundle: {os.path.basename(bundles[-1])} ({age_h:.1f} ч, {os.path.getsize(bundles[-1])//1024//1024}MB)")
    if age_h >= 26:
        problems.append('bundle старше 26 ч — обновить: git bundle create /home/z/backups/sanity-monitor-$(date -u +%Y%m%d_%H%M).bundle sanity-monitor')
else:
    print('  [DEAD] bundle отсутствует')
    problems.append('bundle отсутствует')

# === ИТОГ ===
if not problems:
    print('>>> STATE HEALTHY — все линии в норме')
    sys.exit(0)

print(f'>>> PROBLEMS: {problems}')

if not recover_needed or '--recover' not in sys.argv:
    if recover_needed:
        print('>>> RECOVERY RECOMMENDED: python3 tools/state_healthcheck.py --recover')
    sys.exit(1)

# === RECOVERY: вытяжка с Гита ===
print('\n=== RECOVERY: clone -b %s %s ===' % (BRANCH, ORIGIN_URL))
tmp = '/tmp/sanity_recovery'
sh(f'rm -rf {tmp}', cwd='/tmp')
rc, out = sh(f'git clone -b {BRANCH} --single-branch {ORIGIN_URL} {tmp}', cwd='/tmp', timeout=300)
print(f'clone: rc={rc}')
if rc != 0:
    print(f'CLONE FAILED: {out[:300]} — ручная помощь автора нужна (сеть/репо)')
    sys.exit(2)

# Перенос контента (кроме .git) в PROJ
if not os.path.isdir(PROJ):
    os.makedirs(PROJ, exist_ok=True)
rc, out = sh(f'rsync -a --exclude .git {tmp}/ {PROJ}/', cwd='/tmp', timeout=120)
print(f'rsync: rc={rc}')
# git-каталог: если у PROJ .git мёртв — забираем из клона
rc, out = sh('git fsck --no-dangling 2>&1 | head -2')
if rc != 0:
    sh(f'rm -rf {PROJ}/.git')
    sh(f'cp -a {tmp}/.git {PROJ}/.git')
    print('git dir restored from clone')
sh(f'rm -rf {tmp}', cwd='/tmp')

# Финальная проверка
rc, branch = sh('git branch --show-current')
print(f'>>> RECOVERY DONE: branch={branch.strip()}')
for f in KEY_FILES:
    p = os.path.join(PROJ, f)
    print(f"  [{'OK' if os.path.isfile(p) else 'STILL DEAD'}] {f}")
print('NOTE: если ~/.git-credentials отсутствовал — push недоступен до нового токена от автора (коммить локально, push pending).')
