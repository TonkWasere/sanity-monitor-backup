#!/usr/bin/env python3
# rescan54_60b_phase2.py — Task 54-60 phase 2: OP (near=1) для NEW:
# 196652 «Загадочный тайник на Агрокомлексе» (cc=4, 13:35), 196650 «Мёртвый чат»
# (cc=12, 13:34), 196613 «Опрос на ОТС» (news-NEW, 17.10 16:58 — окно потери 54-37..54-59)
import json, os, urllib.request, time, datetime, re

TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'

def get(url, name, validate_json=True):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}'); return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        if validate_json:
            json.loads(body)
        print(f'OK {name} ({len(body)}B)')
        return True
    except Exception as e:
        print(f'FAIL {name}: {e}')
        return False

def posts_of(fname):
    try:
        d = json.load(open(os.path.join(OUT, fname)))
    except Exception as e:
        print(f'PARSE FAIL {fname}: {e}'); return []
    data = d.get('data')
    items = data if isinstance(data, list) else [data] if data else []
    out = []
    for i in items:
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    return out

def head_text(p, n=150):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or ''
    if not t:
        t = a.get('contentHtml') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

for tid in (196652, 196650, 196613):
    fn = f'discussion_{tid}_near1_{TS}.json'
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', fn); time.sleep(1)
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        print(f"[{tid}] title={aa.get('title')} cc={aa.get('commentCount')} lastPostNumber={aa.get('lastPostNumber')} createdAt={aa.get('createdAt','')[:16]}")
    except Exception as e:
        print(f'[{tid}] attrs fail {e}')
    for p in sorted(posts_of(fn), key=lambda p: p.get('attributes', {}).get('number') or 0)[:3]:
        a = p.get('attributes', {})
        print(f"  #{a.get('number')} {a.get('createdAt','')[:16]} :: {head_text(p)}")

print(f'\nTS={TS}')
