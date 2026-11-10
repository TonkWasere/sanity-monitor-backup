#!/usr/bin/env python3
"""wipe_sentinel.py — WIPE-детектор для трёх линий (v1, 10.11.2026, после WIPE-#61).

Принцип: origin/sanity-monitor — внешний сентинел, недоступный для отката VM.
После idle-эвикции платформа возвращает VM к базе 19.10 (HEAD 71c70b8) —
локальный HEAD оказывается ПОЗАДИ origin. Это и есть детект (см.
output/08_monitoring/WIPE_FORENSICS_20261109.md, H1).

gate(repo) — вызывать в каждом тике ПОСЛЕ flock-лока и ДО тяжёлой работы:
  ok     — HEAD == origin HEAD, или HEAD впереди origin (недопуш прошлого тика)
  wipe   — HEAD позади origin на N коммитов, или diverged → exit 5 + ранбук R2
  creds  — fetch упал на авторизации → креды сожжены → exit 4 + ранбук R1
  net    — сеть/хост недоступны → НЕ блокируем тик (не наша вина), exit 0

mark(repo) — после прохождения gate: /tmp/wipe_last_tick.json (epoch, head,
free_mb). Отсутствие файла на следующем тике = мягкий признак recycle/вайпа
(сообщается, тик не рвётся — сильный детект всё равно по origin).

Не мутирует репозиторий: только read-команды + fetch (blob:none — 7G
evidence_post не скачиваются). Exit-коды: 0 ok/net/other, 4 creds, 5 wipe.
"""
import json
import os
import subprocess
import sys
import time

REPO = '/home/z/my-project'
BRANCH = 'sanity-monitor'
SENTINEL_PATH = '/tmp/wipe_last_tick.json'
CRED_PATH = os.path.expanduser('~/.git-credentials')

R2_RUNBOOK = (
    "R2 (нулевая материализация, ~2 мин):\n"
    "  git update-ref refs/heads/sanity-monitor origin/sanity-monitor\n"
    "  git read-tree HEAD\n"
    "  git ls-files -z output/evidence_post | git update-index -z --skip-worktree --stdin\n"
    "  git diff --name-only -z -- . ':(exclude)output/evidence_post' | git checkout-index -f -z --stdin\n"
    "  rm -rf output/evidence_post && mkdir -p output/evidence_post\n"
    "  (первый прогон checkout-index может потерять хвост — повторить diff|checkout-index;\n"
    "   критерий успеха: git status --short | wc -l == 0)\n"
    "  Затем: python3 tools/restore_state_from_repo.py  → /tmp/prev_lpn_*.json\n"
)

R1_RUNBOOK = (
    "R1 (креды, ~2 мин):\n"
    "  python3 tools/mega_fetch.py            # → /tmp/mega_restore/PAT_VAULT_LOCAL.md\n"
    "  printf 'https://TonkWasere:%s@github.com/\\n' \"$TOKEN\" > ~/.git-credentials && chmod 600\n"
    "  curl -s -o /dev/null -w '%{http_code}' -H \"Authorization: token $TOKEN\" https://api.github.com/user  # → 200\n"
    "  shred -u /tmp/mega_restore/PAT_VAULT_LOCAL.md\n"
    "  (если fetch origin уже проходил — R1 не нужен, creds живы)\n"
)


def _run(cmd, cwd, timeout=90):
    env = dict(os.environ)
    env['GIT_TERMINAL_PROMPT'] = '0'          # никогда не висим на промпте кредов
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=timeout, env=env)
    return p.returncode, (p.stdout or '').strip(), (p.stderr or '').strip()


def _classify_fetch_err(err):
    e = (err or '').lower()
    auth = ('authentication', '403', 'permission denied', 'could not read username',
            'terminal prompts disabled', 'invalid credentials', 'unauthorized',
            'could not read from remote repository')
    net = ('could not resolve host', 'connection refused', 'connection timed out',
           'network is unreachable', 'timed out', 'temporary failure in name resolution')
    if any(m in e for m in auth):
        # «could not read from remote repository» бывает и при сети — приоритет сетевых маркеров
        if any(m in e for m in net):
            return 'net'
        return 'creds'
    if any(m in e for m in net):
        return 'net'
    return 'other'


def _subj(repo, sha):
    rc, out, _ = _run(['git', 'log', '-1', '--format=%h %s', sha], repo, timeout=20)
    return out[:70] if rc == 0 else sha[:12]


def gate(repo=REPO):
    """Возвращает dict(status=..., detail=...). Печатает баннер+ранбук при аларме."""
    st = {'status': 'ok', 'detail': ''}

    rc, _, err = _run(['git', 'fetch', '--filter=blob:none', '--quiet',
                       'origin', BRANCH], repo, timeout=90)
    if rc != 0:
        kind = _classify_fetch_err(err)
        if kind == 'creds':
            st['status'] = 'creds'
            st['detail'] = f'fetch auth fail: {err[:120]}'
            print(f">>> [WIPE-CREDS] fetch origin упал на авторизации — креды сожжены (признак WIPE)\n"
                  f"    {err[:160]}\n{R1_RUNBOOK}")
        elif kind == 'net':
            st['status'] = 'net'
            st['detail'] = f'fetch net fail (тик продолжаем): {err[:120]}'
            print(f">>> [SENTINEL] сеть недоступна, детект пропускаем: {err[:120]}")
        else:
            st['status'] = 'other'
            st['detail'] = f'fetch fail: {err[:120]}'
            print(f">>> [SENTINEL] fetch упал неясно как (тик продолжаем): {err[:120]}")
        return st

    rc, head, _ = _run(['git', 'rev-parse', 'HEAD'], repo, timeout=20)
    rc2, origin, _ = _run(['git', 'rev-parse', f'origin/{BRANCH}'], repo, timeout=20)
    if rc != 0 or rc2 != 0:
        st['status'] = 'other'
        st['detail'] = 'rev-parse failed'
        return st

    if head == origin:
        st['detail'] = 'HEAD == origin'
        return st

    rc, _, _ = _run(['git', 'merge-base', '--is-ancestor', f'origin/{BRANCH}', 'HEAD'],
                    repo, timeout=20)
    if rc == 0:                                   # origin предок HEAD → мы впереди (недопуш)
        st['detail'] = 'HEAD ahead of origin (недопуш прошлого тика — пуш произойдёт в конце)'
        return st

    rc, n_back, _ = _run(['git', 'rev-list', '--count', f'HEAD..origin/{BRANCH}'],
                         repo, timeout=20)
    st['status'] = 'wipe'
    st['detail'] = (f'local={head[:12]} ({_subj(repo, head)})\n'
                    f'    origin={origin[:12]} ({_subj(repo, origin)})\n'
                    f'    origin впереди на {n_back} коммитов')
    print(f">>> [WIPE-ALARM] ОБНАРУЖЕН ОТКАТ VM: локальный HEAD позади origin!\n"
          f"    {st['detail']}\n{R2_RUNBOOK}"
          f"    ЗАПРЕЩЕНО: tools/state_healthcheck.py --recover (материализует ~7G evidence_post!)\n"
          f"    После R1/R2 — работа тика по LITE-протоколу + worklog-строка WIPE.")
    return st


def soft_check():
    """Мягкий индикатор: /tmp-сентинел отсутствует → VM перезапускалась."""
    if not os.path.exists(SENTINEL_PATH):
        return None
    try:
        return json.load(open(SENTINEL_PATH))
    except Exception:
        return None


def mark(repo=REPO):
    """Best-effort: пишем сентинел тика. Никогда не рвёт тик."""
    try:
        rc, head, _ = _run(['git', 'rev-parse', 'HEAD'], repo, timeout=15)
        free_mb = 0
        try:
            fst = os.statvfs('/')
            free_mb = fst.f_bavail * fst.f_frsize // (1024 * 1024)
        except Exception:
            pass
        data = {'epoch': int(time.time()),
                'iso': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'head': head if rc == 0 else '?',
                'free_mb': free_mb}
        with open(SENTINEL_PATH, 'w') as f:
            json.dump(data, f)
        os.chmod(SENTINEL_PATH, 0o600)
    except Exception:
        pass


if __name__ == '__main__':
    repo = sys.argv[1] if len(sys.argv) > 1 else REPO
    last = soft_check()
    if last is None:
        print('>>> [SENTINEL] /tmp-сентинел отсутствует — VM перезапускалась/первый тик '
              '(мягкий признак, решение по origin-детекту ниже)')
    else:
        age = int(time.time()) - int(last.get('epoch', 0))
        print(f'>>> [SENTINEL] прошлый тик: {last.get("iso")} '
              f'({age // 60} мин назад), head={str(last.get("head"))[:12]}, '
              f'free={last.get("free_mb")}MB')
    res = gate(repo)
    print(f'>>> [SENTINEL] status={res["status"]}')
    sys.exit({'ok': 0, 'net': 0, 'other': 0, 'creds': 4, 'wipe': 5}[res['status']])
