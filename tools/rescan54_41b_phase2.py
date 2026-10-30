#!/usr/bin/env python3
# rescan54_41b_phase2.py — Task 54-41 phase 2: OP новых/оживших тредов окна 17:26
# (196617 «Говнезей», 196618 «Загадочный тайник», revive: 196445 «Наградки)»,
# 196423 «Почему игру крашит?», 196406 «Ломание модельки») + хвосты 196496
# (флейм +25/ч) и 196434 «Колизей открыт для рейтинговых боёв» (news, 17:26).
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
    out = [i for i in items if isinstance(i, dict) and i.get('type') == 'posts']
    out += [i for i in (d.get('included') or []) if isinstance(i, dict) and i.get('type') == 'posts']
    return out

def users_of(fname):
    try:
        d = json.load(open(os.path.join(OUT, fname)))
    except Exception:
        return {}
    users = {}
    for u in (d.get('included') or []):
        if isinstance(u, dict) and u.get('type') == 'users':
            users[u['id']] = u.get('attributes', {}).get('username')
    return users

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

def show(tid, fn, tag, tail_n=6):
    users = users_of(fn)
    pp = posts_of(fn)
    pp = sorted(pp, key=lambda p: p.get('attributes', {}).get('number') or 0)
    sel = pp[:1] if tag == 'OP' else pp[-tail_n:]
    for p in sel:
        a = p.get('attributes', {})
        rel = p.get('relationships', {}) or {}
        ud = (rel.get('user') or {}).get('data') or {}
        uname = users.get(ud.get('id'), '?')
        print(f"  #{a.get('number')} {a.get('createdAt','')[:19]} [{uname}] :: {head_text(p)}")

print('=== NEW/revive OPs (near=1) ===')
for tid, label in ((196617, 'Говнезей'), (196618, 'Загадочный тайник'),
                   (196445, 'Наградки)'), (196423, 'Почему игру крашит?'),
                   (196406, 'Ломание модельки/хитбокса')):
    fn = f'discussion_{tid}_near1_{TS}.json'
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', fn); time.sleep(1)
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        aa = d.get('data', {}).get('attributes', {})
        print(f'[{tid}] «{label}» cc={aa.get("commentCount")} createdAt={aa.get("createdAt","")[:16]}')
        show(tid, fn, 'OP')
    except Exception as e:
        print(f'[{tid}] meta fail {e}')

print('\n=== хвосты движущихся ===')
for tid, label in ((196496, 'Простой пример (флейм)'), (196434, 'Колизей рейтинговые бои (news)')):
    fn = f'discussion_{tid}_near999999_{TS}.json'
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', fn); time.sleep(1)
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        aa = d.get('data', {}).get('attributes', {})
        print(f'[{tid}] «{label}» cc={aa.get("commentCount")} LPN={aa.get("lastPostNumber")}')
        show(tid, fn, 'TAIL')
    except Exception as e:
        print(f'[{tid}] meta fail {e}')

print(f'\nTS={TS}')
