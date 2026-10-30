# rescan54_141b_phase2.py — фаза-2 раунда 54-141 (TS 2233 слой): NEW ×4 (196807/196820/196823/196821)
# + авторство ключевых постов 196810 (#61/#62/#64 — Crios-ответ верификация relationships.user)
import json, os, urllib.request, time, re, datetime

TS = '20261021_2233'
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
        print(f'PARSE FAIL {fname}: {e}'); return [], d
    data = d.get('data')
    items = data if isinstance(data, list) else [data] if data else []
    pp = [i for i in items if isinstance(i, dict) and i.get('type') == 'posts']
    inc = [i for i in (d.get('included') or []) if isinstance(i, dict) and i.get('type') == 'posts']
    return pp + inc, d

def head_text(p, n=150):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or a.get('contentHtml') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

NEW_IDS = [196807, 196820, 196823, 196821]
print('=== ФАЗА-2 54-141: NEW ×4 (near=1 + near999999 ОБА, урок 54-138; перепроверка createdAt, урок 54-136) ===')
ranks = {}
for tid in NEW_IDS:
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)
    for near in ('1', '999999'):
        fn = f'discussion_{tid}_near{near}_{TS}.json'
        try:
            d = json.load(open(os.path.join(OUT, fn)))
            aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
            pp, _ = posts_of(fn)
            groups = {i['id']: (i.get('attributes', {}) or {}).get('nameSingular') for i in (d.get('included') or []) if i.get('type') == 'groups'}
            users = {i['id']: i for i in (d.get('included') or []) if i.get('type') == 'users'}
            opid = ((d.get('data') or {}).get('relationships', {}) or {}).get('user', {}).get('data', {})
            opid = opid.get('id') if isinstance(opid, dict) else None
            u = users.get(opid) or {}
            ua_ = u.get('attributes', {})
            gids = [x.get('id') for x in u.get('relationships', {}).get('groups', {}).get('data', [])]
            ranks[tid] = (ua_.get('username'), [groups.get(g, g) for g in gids], (ua_.get('joinTime') or '?')[:10])
            print(f'[{tid} near{near}] cc={aa.get("commentCount")} LPN={aa.get("lastPostNumber")} createdAt={aa.get("createdAt")} title={aa.get("title","")[:60]}')
            print(f'  OP={ua_.get("username")} groups={[groups.get(g, g) for g in gids]} join={(ua_.get("joinTime") or "?")[:10]}')
            tail = sorted(pp, key=lambda p: (p.get('attributes', {}) or {}).get('number') or 0)
            for p in (tail[:3] if near == '1' else tail[-6:]):
                a = p.get('attributes', {}) or {}
                print(f"  #{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")
        except Exception as e:
            print(f'[{tid} near{near}] fail: {e}')

print('\n=== 196810 авторство #61/#62/#64 (урок 54-137: relationships.user, цитаты обманывают) ===')
pp, d = posts_of(f'discussion_196810_near999999_{TS}.json')
groups = {i['id']: (i.get('attributes', {}) or {}).get('nameSingular') for i in (d.get('included') or []) if i.get('type') == 'groups'}
users = {i['id']: i for i in (d.get('included') or []) if i.get('type') == 'users'}
for p in pp:
    a = p.get('attributes', {}) or {}
    if a.get('number') in (61, 62, 63, 64):
        uid = ((p.get('relationships', {}) or {}).get('user', {}) or {}).get('data', {}) or {}
        uid = uid.get('id')
        u = users.get(uid) or {}
        ua_ = u.get('attributes', {})
        gids = [x.get('id') for x in u.get('relationships', {}).get('groups', {}).get('data', [])]
        print(f"  #{a.get('number')} {a.get('createdAt')} AUTHOR={ua_.get('username')} groups={[groups.get(g, g) for g in gids]} :: {head_text(p)}")

print('\n=== СВОДКА NEW ===')
for tid, (un, gr, jt) in ranks.items():
    print(f'  NEW {tid}: OP={un} groups={gr} join={jt}')
