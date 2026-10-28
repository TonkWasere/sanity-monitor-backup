#!/usr/bin/env python3
# rescan54_44b_phase2.py — Task 54-44 phase 2 (TS 2029): OP near=1 для NEW 196623/196620
# + атрибуция ключевых постов из уже сохранённых снапшотов (без новых GET).
import json, os, datetime, re

TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
PREV_TS = '20261017_2029'

import urllib.request, time

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

# === OP near=1 для NEW тредов ===
for tid in (196623, 196620):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)

def load(fn):
    try:
        return json.load(open(os.path.join(OUT, fn)))
    except Exception as e:
        print(f'PARSE FAIL {fn}: {e}'); return {}

def users_map(d):
    um = {}
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'users':
            um[i.get('id')] = i.get('attributes', {}).get('username') or i.get('attributes', {}).get('slug')
    return um

def posts(d):
    out = []
    data = d.get('data')
    items = data if isinstance(data, list) else [data] if data else []
    for i in items:
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    return out

def author_of(p, um):
    pid = None
    rel = p.get('relationships', {}) or {}
    for r in rel.get('user', {}).get('data', []) if isinstance(rel.get('user', {}).get('data'), list) else ([rel.get('user', {}).get('data')] if rel.get('user', {}).get('data') else []):
        pid = r.get('id') if isinstance(r, dict) else None
    return um.get(pid) or f'uid:{pid}'

# === Атрибуция из снапшотов PREV_TS ===
checks = {
    196612: [26, 27, 28],
    196618: [8, 9, 10, 11, 12],
    196611: [38, 42, 43],
    196572: [43, 44, 45, 46, 47, 48],
    196619: [1, 2, 3],
    196100: [38],
    196434: [10],
    195080: [685, 686, 687, 688],
    196524: [1140, 1143, 1144, 1145],
    196561: [34],
}
for tid, nums in checks.items():
    d = load(f'discussion_{tid}_near999999_{PREV_TS}.json')
    if not d:
        continue
    um = users_map(d)
    print(f'\n=== Атрибуция {tid} ===')
    for p in posts(d):
        n = p.get('attributes', {}).get('number')
        if n in nums:
            t = p.get('attributes', {}).get('contentPlain') or p.get('attributes', {}).get('contentHtml') or ''
            t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', str(t))).strip()[:90]
            print(f'  #{n} :: {author_of(p, um)} :: {p.get("attributes", {}).get("createdAt","")[:16]} :: {t}')

# === OP-сводка NEW ===
for tid in (196623, 196620):
    d = load(f'discussion_{tid}_near1_{TS}.json')
    if not d:
        continue
    um = users_map(d)
    dd = d.get('data', {})
    a = dd.get('attributes', {}) if isinstance(dd, dict) else {}
    print(f'\n=== OP {tid} cc={a.get("commentCount")} created={a.get("createdAt","?")[:16]} ===')
    for p in posts(d)[:4]:
        n = p.get('attributes', {}).get('number')
        t = p.get('attributes', {}).get('contentPlain') or p.get('attributes', {}).get('contentHtml') or ''
        t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', str(t))).strip()[:160]
        print(f'  #{n} :: {author_of(p, um)} :: {p.get("attributes", {}).get("createdAt","")[:16]} :: {t}')

print(f'\nTS_phase2={TS}')
