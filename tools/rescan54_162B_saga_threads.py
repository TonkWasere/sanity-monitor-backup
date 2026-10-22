#!/usr/bin/env python3
"""54-162-B interround: авторская гипотеза — Crios ответил на 'телегу' в треде Винтореза (196855 #7 17:51),
а на посты Санити Команда Проекта НЕ реагировала, кроме мягко-скрытых 2 постов в начале саги (d/195192, d/195660).
Гостевой read-only фетч обоих тредов (near=1 старт + near=999999 хвост) + разбор isHidden у постов Санити."""
import json, os, re, subprocess, sys, time, urllib.request

UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
OUT = 'output/evidence_post'
TS = '20261022_2010'
DIDS = [195192, 195660]

def get(url, name):
    path = os.path.join(OUT, name)
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode('utf-8', 'replace')
        d = json.loads(raw)
        json.dump(d, open(path, 'w'), ensure_ascii=False)
        print(f'  OK {name} ({len(raw)}B)')
        time.sleep(1)
        return d
    except Exception as e:
        print(f'  FAIL {name}: {e}')
        time.sleep(2)
        return None

def strip(html):
    return re.sub('<[^>]+>', '', html or '').replace('&quot;', '"').replace('&amp;', '&').strip()

def analyze(d, label):
    if not d:
        return
    top = d.get('data', {}).get('attributes', {})
    print(f"\n=== {label}: d/{top.get('title')} cc={top.get('commentCount')} LPN={top.get('lastPostNumber')} created={top.get('createdAt')} lastPosted={top.get('lastPostedAt')} hidden={top.get('isHidden')}")
    inc = d.get('included', [])
    users = {x['id']: x.get('attributes', {}) for x in inc if x.get('type') == 'users'}
    posts = [x for x in inc if x.get('type') == 'posts']
    sanity_ids = set()
    for uid, a in users.items():
        un = (a.get('username') or '') + '|' + (a.get('displayName') or '')
        if re.search(r'sanit|санити', un, re.I):
            sanity_ids.add(uid)
            print(f"  USER uid={uid} username={a.get('username')} displayName={a.get('displayName')} joined={a.get('joinedAt')} cc={a.get('commentCount')} warnings={a.get('visibleWarningCount')}")
    for p in sorted(posts, key=lambda p: p.get('attributes', {}).get('number', 0)):
        a = p.get('attributes', {})
        uid = p.get('relationships', {}).get('user', {}).get('data', {}).get('id', '?')
        u = users.get(uid, {})
        un = u.get('username', '?')
        hid = a.get('isHidden')
        hat = a.get('hiddenAt')
        text = strip(a.get('contentHtml'))[:180].replace('\n', ' ')
        mark = ' <<< SANITY' if uid in sanity_ids else ''
        hm = f' HIDDEN@{hat}' if hid else ''
        print(f"  #{a.get('number')} [{un}] {a.get('createdAt','')}{' [CRIOS]' if un == 'Crios' else ''}{hm}{mark} :: {text}")

print('=== 54-162-B: сага-треды d/195192 + d/195660')
for did in DIDS:
    print(f'\n--- d/{did} near=1 (начало саги)')
    d1 = get(f'{BASE}/api/discussions/{did}?near=1', f'discussion_{did}_near1_{TS}.json')
    analyze(d1, f'd/{did} старт')
    print(f'--- d/{did} near=999999 (хвост)')
    d2 = get(f'{BASE}/api/discussions/{did}?near=999999', f'discussion_{did}_near999999_{TS}.json')
    analyze(d2, f'd/{did} хвост')
