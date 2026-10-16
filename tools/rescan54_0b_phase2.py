#!/usr/bin/env python3
# rescan54_0b_phase2.py — Task 54-0 phase 2: OP новых фронт-тредов (196524, 196525) +
# точечная выжимка: 196411 (union/гэпы/#48/#71), 196424 ОТС (tail #88+), 196480 (#125+), 196461 (#162+).
import json, os, urllib.request, time, hashlib, re

TS = '20261016_0029'
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
        t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

def tail_posts(fname, n=8):
    pp = sorted(posts_of(fname), key=lambda p: p.get('attributes', {}).get('number') or 0)
    for p in pp[-n:]:
        a = p.get('attributes', {})
        print(f"  #{a.get('number')} {a.get('createdAt','')[:19]} :: {head_text(p)}")
    return pp

# === OP новых ===
get(f'{BASE}/api/discussions/196524?page[near]=1', f'discussion_196524_near1_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196525?page[near]=1', f'discussion_196525_near1_{TS}.json'); time.sleep(1)

for tid, title in ((196524, 'Мне позвонили. Я признался (cc=26!)'), (196525, 'кто пойдет играть в кое что очень интересное (cc=2)')):
    print(f'\n===== OP {tid}: {title} =====')
    try:
        d = json.load(open(os.path.join(OUT, f'discussion_{tid}_near1_{TS}.json')))
        aa = d.get('data', {}).get('attributes', {})
        print(f"  title={aa.get('title')} cc={aa.get('commentCount')} createdAt={aa.get('createdAt','')[:19]} tags={[t.get('attributes',{}).get('slug') if isinstance(t,dict) else t for t in []]}")
    except Exception as e:
        print(f'  attrs fail: {e}')
    pp = posts_of(f'discussion_{tid}_near1_{TS}.json')
    pp = sorted(pp, key=lambda p: p.get('attributes', {}).get('number') or 0)
    for p in pp[:4]:
        a = p.get('attributes', {})
        print(f"  OP#{a.get('number')} {a.get('createdAt','')[:19]} :: {head_text(p, 220)}")

# === 196411: union, gaps, #48 canon, хвост (#71+?) ===
print('\n===== 196411 union-карта / гэпы / #48 =====')
p411 = posts_of(f'discussion_196411_near999999_{TS}.json')
union = {}
for off in ('off0', 'off20', 'off40'):
    for p in posts_of(f'postsindex_196411_{off}_{TS}.json'):
        n = p.get('attributes', {}).get('number')
        if n: union[n] = p
for p in p411:
    n = p.get('attributes', {}).get('number')
    if n: union[n] = p
nums = sorted(union)
gaps = sorted(set(range(1, nums[-1] + 1)) - set(nums))
print(f'union 196411 = 1..{nums[-1]} ({len(nums)} живых), гэпы: {gaps}')
c48 = 0
for n, p in sorted(union.items()):
    if n == 48:
        h = hashlib.sha256((p['attributes'].get('contentHtml') or '').encode()).hexdigest()
        rx = sum((p['attributes'].get('reactionCounts') or {}).values())
        print(f"#48 sha256 {h[:16]}... {'CANON OK' if h == CANON48 else '!!! ИЗМЕНИЛСЯ'} rx={rx}")
        c48 += 1
print(f'tail 196411 (живые последние):')
for n in nums[-6:]:
    a = union[n].get('attributes', {})
    print(f"  #{n} {a.get('createdAt','')[:19]} :: {head_text(union[n], 120)}")

# === 196424 ОТС tail ===
print('\n===== 196424 ОТС (cc=91, сдвиг 00:09 UTC) tail =====')
tail_posts(f'discussion_196424_near999999_{TS}.json', 8)

# === 196480 tail ===
print('\n===== 196480 tail (#125+) =====')
tail_posts(f'discussion_196480_near999999_{TS}.json', 5)

# === 196461 tail ===
print('\n===== 196461 tail =====')
tail_posts(f'discussion_196461_near999999_{TS}.json', 3)

print(f'\nTS={TS}')
