#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# phase2_54_138.py — (1) NEW 196817 «Культисты в Зоне»: OP near=1 БЕЗ include (урок 54-131)
# + полный снап near=999999 (тред появился ПОСЛЕ генерации rescan54_138 — в кортеже его не было);
# (2) контроль-снап 196810 near=41 (хвост абус-обсуждения после «Зарепортил» #33).
import json, re, time, urllib.request
from datetime import datetime, timezone

TS = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
OUT = '/home/z/my-project/output/evidence_post'
BASE = 'https://forum.exbo.net'


def get(url, name):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(f'{OUT}/{name}', 'wb').write(body)
        json.loads(body)
        print(f'OK {name} ({len(body)}B)')
        return True
    except Exception as e:  # noqa: BLE001
        print(f'FAIL {name}: {e}')
        return False


def strip(h):
    t = re.sub(r'<blockquote[^>]*>', ' [Q] ', h or '')
    t = re.sub(r'<cite[^>]*>', ' @{ ', t)
    t = re.sub(r'</cite>', ' }@ ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def dump(tid, near):
    d = json.load(open(f'{OUT}/discussion_{tid}_near{near}_{TS}.json'))
    posts = [i for i in (d.get('included') or []) if i.get('type') == 'posts']
    users = {i['id']: (i.get('attributes', {}) or {}).get('username')
             for i in (d.get('included') or []) if i.get('type') == 'users'}
    groups = {i['id']: (i.get('attributes', {}) or {}).get('nameSingular')
              for i in (d.get('included') or []) if i.get('type') == 'groups'}
    ug = {}
    for i in (d.get('included') or []):
        if i.get('type') == 'users':
            gids = [x.get('id') for x in (i.get('relationships', {}) or {}).get('groups', {}).get('data', [])]
            ug[i['id']] = [groups.get(g, g) for g in gids]
    rows = []
    for p in posts:
        a = p.get('attributes', {}) or {}
        uid = ((p.get('relationships', {}) or {}).get('user', {}) or {}).get('data', {}) or {}
        uid = uid.get('id')
        rows.append((a.get('number', 0), a.get('createdAt', '')[:16],
                     users.get(uid, uid or '?'), ug.get(uid, []), strip(a.get('contentHtml') or '')))
    return sorted(rows)


print('===== ФАЗА-2: NEW 196817 — OP near=1 БЕЗ include + полный снап near=999999 =====')
get(f'{BASE}/api/discussions/196817?page[near]=1', f'discussion_196817_near1_{TS}.json')
time.sleep(1)
get(f'{BASE}/api/discussions/196817?page[near]=999999', f'discussion_196817_near999999_{TS}.json')
time.sleep(1)
try:
    d = json.load(open(f'{OUT}/discussion_196817_near1_{TS}.json'))
    a = (d.get('data', {}) or {}).get('attributes', {}) or {}
    rows = dump(196817, 1)
    op = rows[0] if rows else None
    print(f'  [196817] cc={a.get("commentCount")} LPN={a.get("lastPostNumber")} createdAt={a.get("createdAt","?")[:16]} title={a.get("title","?")}')
    if op:
        print(f'    OP #{op[0]} {op[1]} BY {op[2]} {op[3]} :: {op[4][:180]}')
    for r in rows[1:5]:
        print(f'    #{r[0]} {r[1]} BY {r[2]} {r[3]} :: {r[4][:110]}')
except Exception as e:  # noqa: BLE001
    print(f'  [196817] parse fail: {e}')

print('\n===== 196810 хвост #34-#41: авторы (офиц. ответ после Crios #33?) =====')
try:
    for num, ts, user, gr, txt in dump(196810, 999999):
        if num and num >= 34:
            print(f'  #{num} {ts} BY {user} {gr} :: {txt[:120]}')
except Exception as e:  # noqa: BLE001
    print(f'  parse fail: {e}')
print(f'\nTS={TS}')
