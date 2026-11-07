#!/usr/bin/env python3
# Recovery #6 (wipe #16 ~14:0x UTC 07.11): HEAD→19.10, коммиты bfd65ab4..8b77d42d
# уничтожены, /tmp и /home/z/backups снесены. НОВОЕ: PAT из MEGA-волта автора
# настроен (~/.git-credentials) — первый push за 3 дня возможен.
# Базовая линия origin = cfef89c9 (04.11 15:45). Данные 05-07.11 — chat-replay.
import json, subprocess, urllib.request, datetime, os

REPO = '/home/z/my-project'
MON = os.path.join(REPO, 'output/08_monitoring')
ORIGIN_REF = 'origin/sanity-monitor'

def origin_show(path):
    r = subprocess.run(['git', 'show', f'{ORIGIN_REF}:{path}'], cwd=REPO,
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f'origin show fail: {path}: {r.stderr[:120]}')
    return r.stdout

restore = [
    'worklog.md',
    'output/08_monitoring/ledger.md',
    'output/08_monitoring/YOUNG_JOURNAL.md',
    'output/08_monitoring/young_threads.json',
    'output/08_monitoring/ext_sources_state.json',
    'output/08_monitoring/GIT_AUTOMATION.md',
    'output/08_monitoring/state_snapshots/prev_lpn_541.json',
    'output/08_monitoring/state_snapshots/prev_lpn_542.json',
]
for p in restore:
    full = os.path.join(REPO, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    data = origin_show(p)
    with open(full, 'wb') as f:
        f.write(data)
    print(f'RESTORED {p} ({len(data)}B)')

tools = ['counter_sweep.py', 'ext_sources.py', 'snap15_young.py',
         'snapnew35.py', 'secret_guard.py', 'state_healthcheck.py']
os.makedirs(os.path.join(REPO, 'tools'), exist_ok=True)
for f in tools:
    data = origin_show(f'tools/{f}')
    with open(os.path.join(REPO, 'tools', f), 'wb') as fh:
        fh.write(data)
    print(f'RESTORED tools/{f} ({len(data)}B)')

# Young-стейт: точные данные по API (read-only)
YOUNG_ALL = ['197704','197705','197706','197707','197708','197709','197710',
             '197711','197712','197713','197714','197715','197716']
API = 'https://forum.exbo.net/api/discussions/{}'
now = datetime.datetime.now(datetime.timezone.utc)
entries = {}
for tid in YOUNG_ALL:
    try:
        req = urllib.request.Request(API.format(tid),
                                     headers={'User-Agent': 'sanity-monitor/1.0'})
        with urllib.request.urlopen(req, timeout=20) as r:
            payload = json.load(r)
        d = payload['data']
        a = d['attributes']
        op = '?'
        rel = (d.get('relationships') or {}).get('user')
        if rel:
            uid = rel['data']['id']
            for inc in payload.get('included', []):
                if inc.get('type') == 'users' and inc.get('id') == uid:
                    op = inc['attributes'].get('username', '?')
                    break
        created = a['createdAt']
        cdt = datetime.datetime.fromisoformat(created)
        until = (cdt + datetime.timedelta(hours=2)).isoformat().replace('+00:00', 'Z')
        entries[str(tid)] = {
            'title': a.get('title', '?'), 'slug': a.get('slug', f'{tid}-x'),
            'createdAt': created, 'op_user': op,
            'stm': str(op).lower().startswith('stm:'),
            'discovered_at': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'source': 'recon-wipe16', 'until_ts': until,
            'last_lpn': int(a.get('lastPostNumber', 0)),
            'last_cc': int(a.get('commentCount', 0)), 'checks': 0,
        }
    except Exception as e:
        print(f'FAIL {tid}: {e}')

# TTL-разделение на момент реконструкции
active, graduated = {}, {}
for tid, e in entries.items():
    cdt = datetime.datetime.fromisoformat(e['createdAt'])
    if now - cdt > datetime.timedelta(hours=2):
        graduated[tid] = e
    else:
        active[tid] = e
young = {'_meta': {'version': 1,
          'note': 'young queue (recon wipe16, TTL-разделение при реконструкции)'},
         'threads': dict(sorted(active.items())),
         'graduated': dict(sorted(graduated.items()))}
with open(os.path.join(MON, 'young_threads.json'), 'w', encoding='utf-8') as f:
    json.dump(young, f, ensure_ascii=False, indent=1)
print(f'young_threads.json REBUILT: active={sorted(active)} graduated={sorted(graduated)}')

# long30_state: pass_no 186 (последний完成 пасс), prev_n 542 → redo на 15:02-слоте
state = {'pass_no': 186, 'last_pass_utc': '20261107_1332',
         'prev_n': 542, 'force_integrity': False}
with open(os.path.join(MON, 'long30_state.json'), 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=1)
print('long30_state.json: pass_no=186 prev_n=542')

os.makedirs('/home/z/backups', exist_ok=True)
print('RECOVERY-6 CORE DONE')
