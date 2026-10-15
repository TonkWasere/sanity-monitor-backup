#!/usr/bin/env python3
# rescan52_fetch.py — Task 52: пост-откатный форум-проход (новости: Доставки Рюкзаков, «в сторону игроков», фикс скина; караул: 196411/196428/контролы/196062/196078/ТГК) TS (auto UTC).
import json, os, urllib.request, time, hashlib, datetime

TS = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
CANON48 = 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e'

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

def disc_items(fname):
    """Список discussions из /api/discussions* снапа (union data + included)."""
    try:
        d = json.load(open(os.path.join(OUT, fname)))
    except Exception as e:
        print(f'PARSE FAIL {fname}: {e}'); return []
    out = []
    data = d.get('data')
    for i in (data if isinstance(data, list) else [data] if data else []):
        if isinstance(i, dict) and i.get('type') == 'discussions':
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'discussions':
            out.append(i)
    return out

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

import re
def head_text(p, n=110):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or ''
    if not t:
        h = a.get('contentHtml') or ''
        t = h
    if not isinstance(t, str):
        try:
            t = json.dumps(t, ensure_ascii=False)
        except Exception:
            t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

# === ФАЗА 1: витрина новостей + караул ===
get(f'{BASE}/api/discussions?filter[tag]=news&sort=-lastPostedAt&page[size]=50&page[offset]=0', f'tagnews_off0_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions?page[offset]=0', f'frontindex_off0_{TS}.json'); time.sleep(1)
# караул-треды
get(f'{BASE}/api/discussions/196411?page[near]=999999', f'discussion_196411_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196428?page[near]=999999', f'discussion_196428_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196078?page[near]=999999', f'discussion_196078_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196062?page[near]=999999', f'discussion_196062_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196315?page[near]=999999', f'discussion_196315_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196415?page[near]=999999', f'discussion_196415_near999999_{TS}.json'); time.sleep(1)
get('https://t.me/s/stalzone', f'tg_stalzone_page0_{TS}.html', validate_json=False)

# === РЕЗЮМЕ ФАЗЫ 1 ===
print('\n===== NEWS TAG INDEX (off0) =====')
news = disc_items(f'tagnews_off0_{TS}.json')
seen = set()
for i in news:
    a = i.get('attributes', {})
    did = i.get('id')
    if did in seen: continue
    seen.add(did)
    print(f"  [{did}] {a.get('lastPostedAt','?')[:16]} :: {a.get('title','')[:90]}")

print('\n===== FRONT INDEX (off0) =====')
front = disc_items(f'frontindex_off0_{TS}.json')
seen2 = set()
for i in front:
    a = i.get('attributes', {})
    did = i.get('id')
    if did in seen2: continue
    seen2.add(did)
    print(f"  [{did}] {a.get('lastPostedAt','?')[:16]} cc={a.get('commentCount')} :: {a.get('title','')[:80]}")

print('\n===== 196411 / #48 =====')
p411 = posts_of(f'discussion_196411_near999999_{TS}.json')
try:
    d411 = json.load(open(os.path.join(OUT, f'discussion_196411_near999999_{TS}.json')))
    a411 = d411.get('data', {}).get('attributes', {}) if isinstance(d411.get('data'), dict) else {}
    print(f"[196411] cc={a411.get('commentCount')} lastPostNumber={a411.get('lastPostNumber')} locked={a411.get('isLocked')}")
except Exception as e:
    print(f'[196411] attrs fail {e}')
p48 = next((p for p in p411 if p.get('attributes', {}).get('number') == 48), None)
if not p48:
    print('>>> #48 ОТСУТСТВУЕТ — СНОС/HIDE!')
else:
    a = p48['attributes']
    h = hashlib.sha256((a.get('contentHtml') or '').encode()).hexdigest()
    print(f">>> #48: sha256 {h[:16]}... {'CANON OK' if h == CANON48 else '!!! ИЗМЕНИЛСЯ'} hiddenAt={a.get('hiddenAt')} isApproved={a.get('isApproved')} rx={sum((a.get('reactionCounts') or {}).values())} likes={a.get('likesCount')}")
tail411 = sorted(p411, key=lambda p: p.get('attributes', {}).get('number') or 0)[-6:]
for p in tail411:
    a = p.get('attributes', {})
    print(f"  #411-{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")

print('\n===== 196428 =====')
p428 = posts_of(f'discussion_196428_near999999_{TS}.json')
try:
    d428 = json.load(open(os.path.join(OUT, f'discussion_196428_near999999_{TS}.json')))
    a428 = d428.get('data', {}).get('attributes', {}) if isinstance(d428.get('data'), dict) else {}
    print(f"[196428] cc={a428.get('commentCount')} lastPostNumber={a428.get('lastPostNumber')} locked={a428.get('isLocked')}")
except Exception as e:
    print(f'[196428] attrs fail {e}')
tail428 = sorted(p428, key=lambda p: p.get('attributes', {}).get('number') or 0)[-5:]
for p in tail428:
    a = p.get('attributes', {})
    print(f"  #428-{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")

print('\n===== 196078 (магпулы) =====')
p78 = posts_of(f'discussion_196078_near999999_{TS}.json')
try:
    d78 = json.load(open(os.path.join(OUT, f'discussion_196078_near999999_{TS}.json')))
    a78 = d78.get('data', {}).get('attributes', {}) if isinstance(d78.get('data'), dict) else {}
    print(f"[196078] cc={a78.get('commentCount')} sticky={a78.get('sticky')} lastPostNumber={a78.get('lastPostNumber')}")
except Exception as e:
    print(f'[196078] attrs fail {e}')
tail78 = sorted(p78, key=lambda p: p.get('attributes', {}).get('number') or 0)[-5:]
for p in tail78:
    a = p.get('attributes', {})
    print(f"  #078-{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")

print('\n===== 196062 =====')
p62 = posts_of(f'discussion_196062_near999999_{TS}.json')
try:
    d62 = json.load(open(os.path.join(OUT, f'discussion_196062_near999999_{TS}.json')))
    a62 = d62.get('data', {}).get('attributes', {}) if isinstance(d62.get('data'), dict) else {}
    print(f"[196062] cc={a62.get('commentCount')} lastPostNumber={a62.get('lastPostNumber')}")
except Exception as e:
    print(f'[196062] attrs fail {e}')
tail62 = sorted(p62, key=lambda p: p.get('attributes', {}).get('number') or 0)[-4:]
for p in tail62:
    a = p.get('attributes', {})
    print(f"  #062-{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")

print('\n===== КОНТРОЛЫ =====')
for tid in (196315, 196415):
    pp = posts_of(f'discussion_{tid}_near999999_{TS}.json')
    try:
        dd = json.load(open(os.path.join(OUT, f'discussion_{tid}_near999999_{TS}.json')))
        aa = dd.get('data', {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
        nums = sorted((p.get('attributes', {}).get('number') or 0) for p in pp)
        last = max((p.get('attributes', {}).get('createdAt') or '' for p in pp), default='')
        print(f"[{tid}] cc={aa.get('commentCount')} lastPostNumber={aa.get('lastPostNumber')} lastCreatedAt={last[:16]} unionTail={nums[-3:] if nums else []}")
    except Exception as e:
        print(f'[{tid}] attrs fail {e}')

print(f'\nTS={TS}')
