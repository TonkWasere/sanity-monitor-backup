#!/usr/bin/env python3
# rescan54_47b_phase2.py — Task 54-47 phase 2 (23:35 UTC 17.10): добор 196610 (front cc 12→21) + атрибуция по снапшотам 2330/2332 локально.
import json, os, urllib.request, time, datetime, re, glob

TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'

def get(url, name):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}'); return
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        json.loads(body)
        print(f'OK {name} ({len(body)}B)')
    except Exception as e:
        print(f'FAIL {name}: {e}')

get(f'{BASE}/api/discussions/196610?page[near]=999999', f'discussion_196610_near999999_{TS}.json'); time.sleep(1)

def load_latest(tid, near):
    fns = sorted(glob.glob(os.path.join(OUT, f'discussion_{tid}_near{near}_*.json')))
    return json.load(open(fns[-1])), fns[-1]

def posts_users(d):
    posts, users = {}, {}
    data = d.get('data')
    items = data if isinstance(data, list) else [data] if data else []
    for i in items + (d.get('included') or []):
        if not isinstance(i, dict): continue
        if i.get('type') == 'posts':
            posts[i.get('attributes', {}).get('number')] = (i.get('attributes', {}), i.get('relationships', {}).get('user', {}).get('data', {}).get('id'))
        elif i.get('type') == 'users':
            users[i.get('id')] = i.get('attributes', {}).get('username') or i.get('attributes', {}).get('displayName')
    return posts, users

def show(tid, near, nums):
    d, fn = load_latest(tid, near)
    posts, users = posts_users(d)
    a = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
    print(f'--- {tid} ({fn[-9:-5]}) cc={a.get("commentCount")} LPN={a.get("lastPostNumber")}')
    for n in nums:
        if n in posts:
            at, uid = posts[n]
            uname = users.get(uid) if uid else None
            if not uname: uname = '-'
            txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', at.get('contentPlain') or at.get('content') or at.get('contentHtml') or ''))[:95]
            print(f'  #{n} {at.get("createdAt","")[:16]} [{uname} id={uid}] stm={str(at.get("steamId") or "")[-6:]} :: {txt}')
        else:
            print(f'  #{n} ОТСУТСТВУЕТ (снесён?)')

# атрибуция новых постов раунда
show(196524, '999999', [1146, 1147])          # Глеб +2
show(196627, '999999', [20, 21, 22, 23, 24, 25])  # соло-поддержка вспышка
show(187993, '999999', [1149, 1150, 1151, 1152, 1153, 1154, 1155, 1156])  # Пульс-мета
show(196623, '999999', [4, 5])                # «Передам» — офиц.?
show(196624, '999999', [28, 29, 30, 31, 32, 33])  # CPU-тред рост
show(196572, '999999', [49, 50])              # сессионки
show(196610, '999999', [13, 14, 15, 16, 17, 18, 19, 20, 21])  # раздача ОТС +9
show(196625, '999999', [9, 10])               # Sig-баг #9 кто-то офиц?
print(f'TS={TS}')
