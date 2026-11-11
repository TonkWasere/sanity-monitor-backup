#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# auto_tick.py — 54-689: автономный тик линии мониторинга БЕЗ чат-агента.
# Вызывается локальным шедулером (mini-services/monitor-scheduler, порт 3031)
# или вручную: python3 tools/auto_tick.py long30|s15|s35
#
# Полный цикл lite-агента:
#   1) disk-fuse (≥70% → rm материализованного evidence, ≥85% → abort)
#   2) линия-скрипт (сам берёт flock cron_lock + wipe_sentinel gate)
#      exit 3 → [SKIP-overlap] (крон-линия удержала лок) — без побочных эффектов
#      exit 5 → self-R2 (нул. материализация до origin) → повтор тика
#      exit 4 → self-R1 (MEGA vault → creds, токен НЕ логируется) → повтор тика
#   3) ext_sources (только long30)
#   4) timeline.jsonl — машинное хранилище событий (для auto_digest)
#   5) ledger [AUTO]-запись (long30) / worklog-строка (s15/s35)
#   6) auto_digest каждый 4-й час (00/04/08/12/16/20 UTC слоты :02)
#   7) secret_guard → git add --sparse -A (проверено 54-689: skip-worktree-missing
#      НЕ стейджатся как deletions) → commit → dual push (fail → push_pending,
#      догоняет следующий тик) → бандл keep-2 (каждый 4-й long30-проход / после R2)
#   8) evidence-инвариант: reflag + rm (на диске 0, в гите всё)
# Red lines: токен никогда не печатается и не коммитится; evidence не остаётся
# на диске; форум read-only; при неясности — коммит локально, пуш откладывается.
import json, os, re, glob, subprocess, sys, time, shutil, urllib.request, urllib.error

REPO = '/home/z/my-project'
MON = os.path.join(REPO, 'output', '08_monitoring')
LEDGER = os.path.join(MON, 'ledger.md')
WORKLOG = os.path.join(REPO, 'worklog.md')
TIMELINE = os.path.join(MON, 'timeline.jsonl')
SCHED = os.path.join(MON, 'scheduler_state.json')
BACKUPS = '/home/z/backups'
EV = os.path.join(REPO, 'output', 'evidence_post')

LINES = {'long30': 'counter_sweep.py', 's15': 'snap15_young.py', 's35': 'snapnew35.py'}


def utc():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def hm():
    return time.strftime('%H:%M', time.gmtime())


def day():
    return time.strftime('%d.%m.%Y', time.gmtime())


def run(cmd, timeout=420, cwd=REPO):
    env = dict(os.environ)
    env['GIT_TERMINAL_PROMPT'] = '0'
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)
        return p.returncode, (p.stdout or ''), (p.stderr or '')
    except subprocess.TimeoutExpired:
        return 124, '', f'timeout {timeout}s'


def run_input(cmd, data, timeout=300):
    env = dict(os.environ)
    env['GIT_TERMINAL_PROMPT'] = '0'
    try:
        p = subprocess.run(cmd, cwd=REPO, input=data, capture_output=True, timeout=timeout, env=env)
        return p.returncode, p.stdout.decode('utf-8', 'ignore'), p.stderr.decode('utf-8', 'ignore')
    except subprocess.TimeoutExpired:
        return 124, '', b'timeout'.decode()


def git(args, timeout=240):
    return run(['git'] + args, timeout=timeout)


def disk_pct():
    st = os.statvfs('/')
    return round((1 - st.f_bavail / st.f_blocks) * 100, 1)


def load_sched():
    try:
        return json.load(open(SCHED, encoding='utf-8'))
    except Exception:
        return {'push_pending': 0, 'wipes': 0, 'r1_runs': 0, 'zero_del_streak': 0, 'ticks': {}}


def save_sched(s):
    os.makedirs(MON, exist_ok=True)
    json.dump(s, open(SCHED, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


# ---------------- evidence-инвариант ----------------
def reflag_evidence():
    rc, files, _ = run(['git', 'ls-files', '-z', 'output/evidence_post'])
    if files:
        run_input(['git', 'update-index', '-z', '--skip-worktree', '--stdin'], files.encode())


def evidence_invariant():
    """reflag всех evidence-путей + очистка диска (инвариант: 0 файлов на диске)."""
    reflag_evidence()
    n = 0
    if os.path.isdir(EV):
        n = len([f for f in os.listdir(EV) if not f.startswith('.')])
        for f in glob.glob(os.path.join(EV, '*')):
            try:
                if os.path.isdir(f):
                    shutil.rmtree(f, ignore_errors=True)
                else:
                    os.remove(f)
            except Exception:
                pass
    os.makedirs(EV, exist_ok=True)
    return n


# ---------------- self-heal ----------------
def self_r1():
    """R1: MEGA vault → creds. Токен НИКОГДА не печатается и не попадает в файлы репо."""
    print('[auto_tick] R1: восстановление кредов из MEGA-хранилища...')
    run([sys.executable, os.path.join(REPO, 'tools', 'mega_fetch.py')], timeout=180)
    vault = '/tmp/mega_restore/PAT_VAULT_LOCAL.md'
    tok = None
    if os.path.exists(vault):
        try:
            txt = open(vault, encoding='utf-8', errors='ignore').read()
            m = re.search(r'(ghp_[A-Za-z0-9]+|github_pat_[A-Za-z0-9_]+)', txt)
            tok = m.group(1) if m else None
        except Exception:
            tok = None
    ok = False
    if tok:
        try:
            req = urllib.request.Request('https://api.github.com/user', headers={
                'Authorization': f'token {tok}', 'User-Agent': 'sanity-auto-tick'})
            ok = (urllib.request.urlopen(req, timeout=25).status == 200)
        except Exception:
            ok = False
    if ok:
        gc = os.path.expanduser('~/.git-credentials')
        with open(gc, 'w') as f:
            f.write(f'https://TonkWasere:{tok}@github.com/\n')
        os.chmod(gc, 0o600)
        git(['config', 'credential.helper', 'store'])
    if os.path.exists(vault):  # shred
        try:
            sz = os.path.getsize(vault)
            with open(vault, 'r+b') as f:
                f.write(os.urandom(sz))
            os.remove(vault)
        except Exception:
            pass
    try:
        os.rmdir('/tmp/mega_restore')
    except OSError:
        pass
    print(f'[auto_tick] R1 done: API {"200 OK" if ok else "FAIL"} (токен не логируется)')
    return ok


def self_r2(reason='wipe'):
    """R2 нулевой материализации: index/HEAD → origin, worktree из индекса (без evidence)."""
    print(f'[auto_tick] R2: восстановление до origin ({reason})...')
    steps = []
    rc, _, _ = git(['reset', '--mixed', 'origin/sanity-monitor'], timeout=120)
    steps.append(('reset--mixed', rc == 0))
    if rc != 0:  # fallback ранбука wipe_sentinel
        git(['update-ref', 'refs/heads/sanity-monitor', 'origin/sanity-monitor'])
        git(['read-tree', 'HEAD'])
        steps.append(('update-ref+read-tree', True))
    for attempt in (1, 2):  # ранбук: первый checkout может терять хвост
        rc, names, _ = run(['git', '-c', 'core.quotepath=off', 'diff', '--name-only', '-z', '--', '.',
                            ':(exclude)output/evidence_post'])
        if names:
            rc2, _, _ = run_input(['git', 'checkout-index', '-f', '-z', '--stdin'], names.encode())
            steps.append((f'checkout#{attempt}', rc2 == 0))
        st = git(['status', '--short'])[1].strip()
        if not st:
            break
    reflag_evidence()
    n = evidence_invariant()
    run([sys.executable, os.path.join(REPO, 'tools', 'restore_state_from_repo.py')], timeout=90)
    st_count = len(git(['status', '--short'])[1].strip().splitlines()) if git(['status', '--short'])[1].strip() else 0
    print(f'[auto_tick] R2 done: {steps}; evidence rm={n}; status={st_count}')
    return st_count == 0


# ---------------- ledger / worklog / timeline ----------------
def last_ledger_no():
    try:
        txt = open(LEDGER, encoding='utf-8', errors='ignore').read()
        nums = [int(x) for x in re.findall(r'^## Запись №(\d+)', txt, re.M)]
        return max(nums) if nums else 0
    except Exception:
        return 0


def append_ledger(text):
    with open(LEDGER, 'a', encoding='utf-8') as f:
        f.write('\n' + text + '\n')


def append_worklog(text):
    with open(WORKLOG, 'a', encoding='utf-8') as f:
        f.write('\n' + text + '\n')


def append_timeline(rec):
    try:
        os.makedirs(MON, exist_ok=True)
        with open(TIMELINE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    except Exception as e:
        print(f'[auto_tick] timeline fail: {e}')


# ---------------- парсеры вывода линий ----------------
SIG_RE = re.compile(r'(NEW-POSTS|DEL-SIG|MIX-SIG|UNHIDE-SIG|ROLLBACK) \[(?:KEY/OWW )?(\d+)\] '
                    r'lpn (\S+)->(\S+) cc (\S+)->(\S+)(?: гэп (\S+))? :: (.*)')


def parse_sweep(out):
    res = {'pass_no': None, 'window': None, 'sig': 0, 'deep_count': 0, 'deep': [], 'oww': None,
           'oww_checked': None, 'integrity': 'нет', 'integrity_lines': [], 'prev_n': None,
           'prev_keys': None, 'newsigs': [], 'special': [], 'newthreads': [], 'vanish': [],
           'oww_fail': [], 'verify': [], 'base_prev': None, 'base_keys': None}
    for ln in out.splitlines():
        m = re.search(r'LONG30 SWEEP pass#(\d+) (\S+) UTC \| база prev_lpn_(\d+) \((\d+) кл\)', ln)
        if m:
            res['pass_no'], res['base_prev'], res['base_keys'] = int(m.group(1)), int(m.group(3)), int(m.group(4))
        m = re.match(r'свин: (\d+) тредов', ln)
        if m:
            res['window'] = int(m.group(1))
        m = re.search(r'SWEEP ИТОГ pass#(\d+): окно (\d+), дельт-сигнатур (\d+),\s*'
                      r'глубоких заходов (\d+) \[([^\]]*)\], OWW (\d+) \(проверено (\d+)\),\s*integrity=(ДА|нет)', ln)
        if m:
            res['pass_no'] = int(m.group(1))
            res['window'], res['sig'] = int(m.group(2)), int(m.group(3))
            res['deep_count'] = int(m.group(4))
            res['deep'] = [int(x) for x in m.group(5).split(',') if x.strip()]
            res['oww'], res['oww_checked'] = int(m.group(6)), int(m.group(7))
            res['integrity'] = m.group(8)
        if ln.startswith('>>> '):
            body = ln[4:]
            m = SIG_RE.match(body)
            if m:
                rec = {'label': m.group(1), 'tid': int(m.group(2)), 'lpn_old': m.group(3),
                       'lpn_new': m.group(4), 'cc_old': m.group(5), 'cc_new': m.group(6),
                       'gap': m.group(7), 'title': m.group(8)[:70]}
                try:
                    rec['dcc'] = int(m.group(6)) - int(m.group(5))
                except Exception:
                    rec['dcc'] = 0
                res['newsigs'].append(rec)
                if m.group(1) != 'NEW-POSTS':
                    res['special'].append(rec)
                continue
            m = re.match(r'NEW-THREAD \[(\d+)\] (\S+) lpn/cc (\d+)/(\d+) :: (.*)', body)
            if m:
                res['newthreads'].append({'tid': int(m.group(1)), 'created': m.group(2),
                                          'lpn': int(m.group(3)), 'cc': int(m.group(4)),
                                          'title': m.group(5)[:70]})
                continue
            m = re.match(r'VANISH-SIG \[(\d+)\](.*)', body)
            if m:
                res['vanish'].append({'tid': int(m.group(1)), 'note': m.group(2).strip()[:70]})
                continue
            m = re.match(r'OWW-FAIL \[(\d+)\]', body)
            if m:
                res['oww_fail'].append(int(m.group(1)))
                continue
            m = re.match(r'NEW-VERIFY \[(\d+)\] (.*)', body)
            if m:
                res['verify'].append({'tid': int(m.group(1)), 'note': m.group(2)[:70]})
                continue
            if body.startswith('CANON') or body.startswith('GG ['):
                res['integrity_lines'].append(body[:110])
                continue
        m = re.search(r'prev_lpn_(\d+)\.json записан \((\d+) кл', ln)
        if m:
            res['prev_n'], res['prev_keys'] = int(m.group(1)), int(m.group(2))
    return res


def parse_lite(out):
    """s15/s35: события (>>> строки), итоговая active/graduated, счётчики."""
    events, total = [], None
    for ln in out.splitlines():
        if ln.startswith('>>> '):
            events.append(ln[4:150])
        m = re.search(r'итог: active=(\d+) graduated=(\d+)(?: recon_add=(\d+))?', ln)
        if m:
            total = {'active': int(m.group(1)), 'graduated': int(m.group(2)),
                     'recon_add': int(m.group(3) or 0)}
        m = re.search(r'DONE SNAP(?:15|35): candidates=(\d+) new=(\d+)', ln)
        if m:
            total = total or {}
            total['candidates'], total['new'] = int(m.group(1)), int(m.group(2))
    return events, total


def parse_ext(out):
    m = re.search(r'итог EXT: events=(\d+)', out)
    fails = [ln[4:110] for ln in out.splitlines() if ln.startswith('FAIL ')]
    return int(m.group(1)) if m else 0, fails


# ---------------- композиция записей ----------------
def fmt_sig_top(newsigs, limit=7, min_dcc=4):
    """Топ движения для ledger: |dcc| >= min_dcc или спец-сигнатуры, по убыванию dcc."""
    rows = [r for r in newsigs if r['label'] != 'NEW-POSTS' or abs(r.get('dcc', 0)) >= min_dcc]
    rows = sorted(rows, key=lambda r: -abs(r.get('dcc', 0)))[:limit]
    out = []
    for r in rows:
        gap = f" гэп {r['gap']}" if r.get('gap') else ''
        out.append(f"[{r['tid']}] «{r['title']}» {r['cc_old']}→{r['cc_new']}{gap}")
    return out


def compose_ledger(res, ext_n, ext_fails, prev_tick_ts, wipe_note):
    p = res['pass_no']
    spec = res['special']
    labels = [r['label'] for r in res['newsigs']]
    n_new = labels.count('NEW-POSTS')
    n_del = sum(1 for x in labels if x in ('DEL-SIG', 'MIX-SIG', 'ROLLBACK'))
    n_unh = labels.count('UNHIDE-SIG')
    if n_del == 0 and n_unh == 0:
        sig_desc = f'все NEW-POSTS ({n_new})'
    else:
        sig_desc = (f'NEW-POSTS {n_new}, DEL {sum(1 for x in labels if x=="DEL-SIG")}, '
                    f'MIX {sum(1 for x in labels if x=="MIX-SIG")}, UNHIDE {n_unh}, '
                    f'ROLLBACK {sum(1 for x in labels if x=="ROLLBACK")}')
    win_txt = ''
    if prev_tick_ts:
        try:
            mins = int((time.time() - time.mktime(time.strptime(prev_tick_ts, '%Y-%m-%dT%H:%M:%SZ'))) // 60)
            win_txt = f'окно ~{mins // 60}ч{mins % 60:02d}м (пред. проход {prev_tick_ts[11:16]})'
        except Exception:
            pass
    parts = [f'## Запись №{last_ledger_no() + 1} — [AUTO-sched] LONG30 pass#{p} {hm()} UTC ({day()})']
    head = f'({win_txt or "окно: пред. время неизвестно"}; скрипт-счётчик #{p}; водитель: локальный шедулер{"; " + wipe_note if wipe_note else ""})'
    parts.append(head)
    ig = res['integrity']
    ig_txt = f'integrity={ig}' + (f' ({"; ".join(res["integrity_lines"][:3])})' if ig == 'ДА' and res['integrity_lines'] else '')
    parts.append(f'Свип: окно {res["window"]}, дельт-сигнатур {res["sig"]} — {sig_desc}, '
                 f'глубоких {res["deep_count"]}{res["deep"]}, OWW {res["oww"]} (проверено {res["oww_checked"]}), {ig_txt}.')
    top = fmt_sig_top(res['newsigs'])
    if top:
        parts.append('Топ-движение: ' + '; '.join(top) + '.')
    if res['verify']:
        parts.append('NEW-VERIFY: ' + '; '.join(f"[{v['tid']}] {v['note']}" for v in res['verify']) + '.')
    if res['newthreads']:
        parts.append('NEW-THREAD ×%d: %s.' % (len(res['newthreads']),
                    '; '.join(f"[{t['tid']}] {t['created'][11:16]} «{t['title']}» {t['lpn']}/{t['cc']}" for t in res['newthreads'])))
    if res['vanish']:
        parts.append('VANISH-SIG: ' + '; '.join(f"[{v['tid']}] {v['note']}" for v in res['vanish']) + '.')
    if res['oww_fail']:
        parts.append(f'OWW-FAIL: {res["oww_fail"]} (сеть/нестабильный GET).')
    ext_txt = f'EXT: events={ext_n}' + (f'; FAIL: {ext_fails[:2]}' if ext_fails else '') + '.'
    parts.append(ext_txt)
    if res['prev_n'] is not None:
        parts.append(f'prev_lpn_{res["prev_n"]}.json записан ({res["prev_keys"]} кл; /tmp + Хранилище keep 2).')
    parts.append('[AUTO-запись шедулера: полные stdout — /tmp/auto_tick_last_long30.log; человеко-аудит — на ближайшем чат-тике]')
    return ' '.join(parts)


# ---------------- git: commit / push / bundle ----------------
def commit_push(message):
    s = load_sched()
    rc, out, _ = run([sys.executable, os.path.join(REPO, 'tools', 'secret_guard.py')], timeout=90)
    if rc != 0:
        print(f'[auto_tick] SECRET GUARD rc={rc} — коммит ОТМЕНЕН: {out[-200:]}')
        return False
    rc, _, _ = git(['add', '--sparse', '-A'])
    if rc != 0:
        print('[auto_tick] git add fail')
        return False
    rc, out, _ = git(['commit', '-m', message])
    committed = rc == 0
    pushed = False
    if committed or s.get('push_pending', 0) > 0:
        rc1, _, e1 = git(['push', 'origin', 'sanity-monitor'], timeout=300)
        rc2, _, e2 = git(['push', 'backup', 'sanity-monitor'], timeout=300)
        pushed = rc1 == 0 and rc2 == 0
        if pushed:
            if s.get('push_pending', 0) > 0:
                append_worklog(f'Task ID: 54-689-auto: push-очередь догнана ({s["push_pending"]} недопуш-тиков) '
                               f'в {hm()} UTC — обе remote зелёные')
            s['push_pending'] = 0
        else:
            s['push_pending'] = s.get('push_pending', 0) + 1
            print(f'[auto_tick] push fail (origin rc={rc1}, backup rc={rc2}) — push_pending={s["push_pending"]}')
    save_sched(s)
    return committed or pushed


def maybe_bundle(force=False):
    """Бандл keep-2: каждый 4-й long30-проход (integrity-окно) или после R2."""
    os.makedirs(BACKUPS, exist_ok=True)
    ts = time.strftime('%Y%m%d_%H%M', time.gmtime())
    dst = os.path.join(BACKUPS, f'sanity-monitor_{ts}.bundle')
    rc, _, _ = git(['bundle', 'create', dst, 'sanity-monitor'], timeout=420)
    if rc != 0:
        print('[auto_tick] bundle create fail')
        return False
    bundles = sorted(glob.glob(os.path.join(BACKUPS, '*.bundle')), key=os.path.getmtime, reverse=True)
    for old in bundles[2:]:
        try:
            os.remove(old)
        except Exception:
            pass
    return True


# ---------------- главная ----------------
def main():
    line = sys.argv[1] if len(sys.argv) > 1 else ''
    if line not in LINES:
        print('usage: auto_tick.py long30|s15|s35')
        return 2
    s = load_sched()
    t0 = time.time()
    print(f'[auto_tick] === {line} slot {hm()} UTC ===')
    wipe_note = ''

    # disk fuse
    dp = disk_pct()
    if dp >= 70:
        n = evidence_invariant()
        print(f'[auto_tick] DISK FUSE {dp}% — evidence rm={n}')
        dp = disk_pct()
        if dp >= 85:
            append_worklog(f'Task ID: 54-689-auto: [sched {line} {hm()}] DISK ≥85% после fuse — тик прерван')
            return 1

    # тик линии (с self-heal)
    script = LINES[line]
    out, rc, healed = '', 0, []
    for attempt in range(3):
        rc, out, err = run([sys.executable, os.path.join(REPO, 'tools', script)], timeout=720)
        open(f'/tmp/auto_tick_last_{line}.log', 'w').write(out + ('\nSTDERR:\n' + err if err else ''))
        if rc == 3:
            append_worklog(f'Task ID: 54-689-auto: [sched {line} {hm()}] [SKIP-overlap] лок занят '
                           f'(крон-линия выполняет тик) — без побочных эффектов')
            s['ticks'][line] = {'ts': utc(), 'rc': 3, 'note': 'skip-overlap'}
            save_sched(s)
            print('[auto_tick] [SKIP-overlap] — крон-линия удержала лок')
            return 0
        if rc == 5:
            print('[auto_tick] WIPE-ALARM (exit 5) → self-R2')
            self_r2('gate exit 5')
            healed.append('R2')
            s['wipes'] = s.get('wipes', 0) + 1
            wipe_note = f'[WIPE-авто-хил R2 {hm()}]'
            save_sched(s)
            continue
        if rc == 4:
            print('[auto_tick] CREDS-ALARM (exit 4) → self-R1')
            if self_r1():
                healed.append('R1')
                s['r1_runs'] = s.get('r1_runs', 0) + 1
                save_sched(s)
                continue
            healed.append('R1-FAIL')
            break
        break

    if rc not in (0,) and not healed:
        # сеть/прочее — линия сама залогировала; фиксируем в worklog если rc не 0
        append_worklog(f'Task ID: 54-689-auto: [sched {line} {hm()}] линия rc={rc} '
                       f'(детали /tmp/auto_tick_last_{line}.log) — без коммита')
        s['ticks'][line] = {'ts': utc(), 'rc': rc}
        save_sched(s)
        return rc or 0

    n_ev = 0  # evidence-инвариант выполняется ПОСЛЕ commit_push (файлы должны попасть в коммит)

    # --- long30: sweep + ext ---
    if line == 'long30':
        res = parse_sweep(out)
        rc_e, out_e, _ = run([sys.executable, os.path.join(REPO, 'tools', 'ext_sources.py')], timeout=420)
        ext_n, ext_fails = parse_ext(out_e)
        open('/tmp/auto_tick_last_ext.log', 'w').write(out_e)
        prev_ts = (s.get('ticks', {}).get('long30', {}) or {}).get('ts')
        entry = compose_ledger(res, ext_n, ext_fails, prev_ts, wipe_note)
        append_ledger(entry)
        streak = s.get('zero_del_streak', 0)
        if not res['special']:
            streak += 1
        else:
            streak = 0
        s['zero_del_streak'] = streak
        top = fmt_sig_top(res['newsigs'], limit=10, min_dcc=3)
        append_worklog(f'Task ID: 54-689-auto: [sched long30 {hm()}] pass#{res["pass_no"]}: '
                       f'{res["sig"]} дельт ({streak}-й проход ноль DEL/MIX/UNHIDE), NEW-THREAD ×{len(res["newthreads"])}, '
                       f'EXT {ext_n}, base {res["prev_n"]} ({res["prev_keys"]} кл)'
                       + (f'; топ: {" ".join(top[:3])}' if top else ''))
        append_timeline({'ts': utc(), 'line': 'long30', 'pass': res['pass_no'], 'window': res['window'],
                         'sig': res['sig'], 'spec': [{'label': r['label'], 'tid': r['tid'],
                                                      'cc_old': r['cc_old'], 'cc_new': r['cc_new'],
                                                      'gap': r['gap'], 'title': r['title']} for r in res['special']],
                         'newsigs': [{'tid': r['tid'], 'cc_old': r['cc_old'], 'cc_new': r['cc_new'],
                                      'gap': r['gap'], 'title': r['title']} for r in res['newsigs']],
                         'newthreads': res['newthreads'], 'vanish': res['vanish'],
                         'oww_fail': res['oww_fail'], 'ext': ext_n, 'integrity': res['integrity'],
                         'healed': healed, 'prev_n': res['prev_n'], 'prev_keys': res['prev_keys']})
        # digest каждый 4-й час (00/04/08/12/16/20 UTC, слот :02)
        now = time.gmtime()
        if now.tm_hour % 4 == 0 and now.tm_min < 10:
            rc_d, out_d, err_d = run([sys.executable, os.path.join(REPO, 'tools', 'auto_digest.py')], timeout=180)
            if rc_d == 0:
                print('[auto_tick] digest выпущен')
            else:
                print(f'[auto_tick] DIGEST FAIL rc={rc_d}: {(err_d or out_d)[-200:]}')
                append_worklog(f'Task ID: 54-689-auto: [sched] DIGEST FAIL rc={rc_d}: '
                               f'{((err_d or out_d)[-120:]).strip()}')
        msg = (f'auto long30 {hm()} UTC: pass#{res["pass_no"]}: {res["sig"]} дельт '
               f'({"все NEW-POSTS" if not res["special"] else "spec: " + ",".join(r["label"] for r in res["special"][:4])}), '
               f'NEW-THREAD {len(res["newthreads"])}, deep {res["deep_count"]}, EXT {ext_n}, '
               f'base {res["prev_n"]} ({res["prev_keys"]}); [sched]')
    else:
        events, total = parse_lite(out)
        if line == 's15' and events:
            append_worklog(f'Task ID: 54-689-auto: [sched s15 {hm()}] events={len(events)}: '
                           + ' | '.join(e[:60] for e in events[:4])
                           + (f'; active={total["active"]} grad={total["graduated"]}' if total else ''))
        elif line == 's35':
            nn = (total or {}).get('new', 0)
            if nn or events:
                append_worklog(f'Task ID: 54-689-auto: [sched s35 {hm()}] new={nn} '
                               f'candidates={(total or {}).get("candidates", "?")}: '
                               + ' | '.join(e[:60] for e in events[:3]))
        append_timeline({'ts': utc(), 'line': line, 'events': events[:12], 'total': total, 'healed': healed})
        msg = (f'auto {line} {hm()} UTC: events={len(events)} '
               f'({(total or {}).get("new", "") and "new=" + str(total["new"]) or "молодые"}); [sched]')

    healed_txt = '+'.join(healed) if healed else ''
    if healed:
        msg += f'; {healed_txt}'
    # evidence: add ДО инварианта (файлы должны попасть в коммит), инвариант после push
    committed = commit_push(msg)
    if committed:
        n2 = evidence_invariant()
        print(f'[auto_tick] evidence invariant: rm={n2}')
    # бандл: каждый 4-й long30-проход или после авто-хила
    if line == 'long30' and committed:
        pass_no_stored = None
        try:
            m = re.search(r'pass#(\d+)', msg)
            pass_no_stored = int(m.group(1)) if m else None
        except Exception:
            pass
        if (pass_no_stored and pass_no_stored % 4 == 0) or 'R2' in healed:
            ok = maybe_bundle()
            print(f'[auto_tick] bundle: {"OK" if ok else "FAIL"} (keep-2)')
    s['ticks'][line] = {'ts': utc(), 'rc': 0, 'dur_s': round(time.time() - t0),
                        'pass': pass_no_stored if line == 'long30' else None,
                        'note': f'healed={healed_txt}' if healed else 'ok'}
    s['last_tick'] = {'ts': utc(), 'line': line, 'dur_s': round(time.time() - t0)}
    save_sched(s)
    print(f'[auto_tick] DONE {line} за {round(time.time() - t0)}s')
    return 0


if __name__ == '__main__':
    sys.exit(main())
