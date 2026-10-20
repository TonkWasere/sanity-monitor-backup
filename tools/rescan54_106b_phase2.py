#!/usr/bin/env python3
# rescan54_106b_phase2.py — Task 54-106: phase-2 OP-проверка NEW-тредов фронта
# (урок 54-69: сверять createdAt перед «NEW ×N»)

import json, os, re, time, urllib.request, datetime

TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
OP_TARGETS = [196737]      # near=1: OP-верификация NEW
MID_TARGETS = []

def get(url, name):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}'); return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        json.loads(body)
        print(f'OK {name} ({len(body)}B)')
        return True
    except Exception as e:
        print(f'FAIL {name}: {e}')
        return False

def clean(t, n=150):
    t = re.sub(r'<[^>]+>', ' ', t or '')
    return re.sub(r'\s+', ' ', t).strip()[:n]

def dump_thread(tid, near, head_n=4, tail_n=3):
    near_s = str(near)
    fn = f'discussion_{tid}_near{near_s}_{TS}.json'
    ok = get(f'{BASE}/api/discussions/{tid}?page[near]={near_s}', fn); time.sleep(1)
    if not ok:
        print(f'[{tid}] FETCH FAIL'); return
    d = json.load(open(os.path.join(OUT, fn)))
    a = d.get('data', {}).get('attributes', {})
    print(f"[{tid}] title={a.get('title')!r} createdAt={a.get('createdAt')} cc={a.get('commentCount')} "
          f"lastPostNumber={a.get('lastPostNumber')} locked={a.get('isLocked')}")
    users = {u.get('id'): u.get('attributes', {}).get('displayName')
             for u in (d.get('included') or []) if u.get('type') == 'users'}
    posts = [i for i in ([d.get('data')] if isinstance(d.get('data'), dict) else []) if i.get('type') == 'posts']
    posts += [i for i in (d.get('included') or []) if i.get('type') == 'posts']
    posts = sorted(posts, key=lambda p: p.get('attributes', {}).get('number') or 0)
    for p in posts[:head_n]:
        pa = p.get('attributes', {})
        rel = (p.get('relationships') or {}).get('user') or {}
        data = rel.get('data') if isinstance(rel, dict) else None
        if isinstance(data, dict):
            data = [data]
        author = users.get((data[0].get('id') if data else ''), '?')
        print(f"  #{pa.get('number')} {pa.get('createdAt')} [{author}] :: {clean(pa.get('contentPlain') or pa.get('contentHtml'))}")
    if len(posts) > head_n + tail_n:
        print('  ...')
    for p in posts[-tail_n:]:
        pa = p.get('attributes', {})
        rel = (p.get('relationships') or {}).get('user') or {}
        data = rel.get('data') if isinstance(rel, dict) else None
        if isinstance(data, dict):
            data = [data]
        author = users.get((data[0].get('id') if data else ''), '?')
        print(f"  #{pa.get('number')} {pa.get('createdAt')} [{author}] :: {clean(pa.get('contentPlain') or pa.get('contentHtml'))}")

print('=== OP-верификация NEW (near=1) ===')
for tid in OP_TARGETS:
    dump_thread(tid, 1)
print('\n=== Добор середины (fast-rule вручную) ===')
for tid, mid in MID_TARGETS:
    dump_thread(tid, mid, head_n=3, tail_n=3)
print(f'\nTS={TS}')
