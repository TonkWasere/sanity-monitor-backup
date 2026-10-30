# check54_135b_getgood.py — межраундовая верификация 17:0x UTC 21.10 (между 54-135 и 54-136).
# ИНТЕЛ АВТОРА (источник: UI-элемент «Уведомления о новых взаимодействиях с постами аккаунта»):
# новые реакции на Санити-постах = u/GetGood; он прогулялся по ВСЕМ постам автора, до которых
# смог добраться. Задача скрипта: (1) замер #14590/#14591 в 159759 гостем (likes/rx сейчас);
# (2) проверка других постов автора (#69 в 195574, #381 в 195660, канон #48 в 196411) — следы
# прогулки GetGood (дельта likes/rx); (3) попытка найти профиль GetGood гостем
# (/api/users?filter[q] — обычно guests запрещено; тогда фиксируем «аттрибуция только из UI автора»).

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

def load_posts(fname):
    try:
        d = json.load(open(os.path.join(OUT, fname)))
    except Exception as e:
        print(f'PARSE FAIL {fname}: {e}'); return [], {}, {}
    users, posts = {}, []
    data = d.get('data')
    items = data if isinstance(data, list) else [data] if isinstance(data, dict) else []
    for i in items + list(d.get('included') or []):
        if not isinstance(i, dict):
            continue
        if i.get('type') == 'posts':
            posts.append(i)
        elif i.get('type') == 'users':
            users[i.get('id')] = (i.get('attributes', {}) or {}).get('username') or i.get('id')
    return posts, users, d

def dump_thread(tid, near, targets, label):
    fn = f'discussion_{tid}_near{near}_{TS}.json'
    get(f'{BASE}/api/discussions/{tid}?page[near]={near}', fn); time.sleep(1)
    posts, users, d = load_posts(fn)
    aa = (d.get('data', {}) or {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
    print(f'--- [{label}] d/{tid} cc={aa.get("commentCount")} LPN={aa.get("lastPostNumber")} locked={aa.get("isLocked")}')
    got = {}
    for p in posts:
        a = p.get('attributes', {}) or {}
        n = a.get('number') or 0
        if n in targets:
            uid = p.get('relationships', {}).get('user', {}).get('data', {})
            uid = uid.get('id') if isinstance(uid, dict) else None
            rc = a.get('reactionCounts') or {}
            got[n] = True
            print(f"  #{n} {a.get('createdAt','?')[:19]} {users.get(uid,'?')} likes={a.get('likesCount')} rx={rc} :: {re.sub('<[^>]+>',' ',(a.get('contentPlain') or ''))[:80]}")
    for t in targets:
        if t not in got:
            print(f"  #{t} НЕ В ОКНЕ near={near} (нет в included)")
    after = [p for p in posts if ((p.get('attributes', {}) or {}).get('number') or 0) > max(targets)]
    return aa, len(after)

print(f'=== GETGOOD-CHECK TS={TS} ===')
aa1, after1 = dump_thread(159759, 14591, {14590, 14591}, 'ПОСТ САНЕТИ')
print(f'>>> 159759: постов после #14591 в окне: {after1}')
aa2, _ = dump_thread(195574, 69, {69}, 'прецедент-Санити 195574')
aa3, _ = dump_thread(195660, 381, {381}, 'Санити-блок 195660')
aa4, _ = dump_thread(196411, 48, {48}, 'канон #48 196411')
# попытка найти GetGood гостем
get(f'{BASE}/api/users?filter%5Bq%5D=GetGood', f'users_search_getgood_{TS}.json'); time.sleep(1)
try:
    d = json.load(open(os.path.join(OUT, f'users_search_getgood_{TS}.json')))
    items = d.get('data') if isinstance(d.get('data'), list) else []
    if items:
        for u in items:
            a = u.get('attributes', {}) or {}
            print(f"USER: {u.get('id')} {a.get('username')} cc={a.get('commentCount')} disc={a.get('discussionCount')} join={a.get('joinedAt')}")
    else:
        print('USER SEARCH: пусто или запрещено гостю (см. тело файла)')
except Exception as e:
    print(f'USER SEARCH parse fail: {e}')
get(f'{BASE}/api/discussions?filter%5Bq%5D=GetGood&page%5Boffset%5D=0', f'search_getgood_{TS}.json'); time.sleep(1)
try:
    d = json.load(open(os.path.join(OUT, f'search_getgood_{TS}.json')))
    dd = d.get('data') or []
    print(f'DISC SEARCH "GetGood": {len(dd)} тредов')
    for i in dd[:5]:
        a = i.get('attributes', {}) or {}
        print(f"  d/{i.get('id')} «{a.get('title')}» cc={a.get('commentCount')} last={str(a.get('lastPostedAt'))[:19]}")
except Exception as e:
    print(f'DISC SEARCH parse fail: {e}')
print('=== END ===')
