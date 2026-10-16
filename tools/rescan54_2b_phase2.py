#!/usr/bin/env python3
# rescan54_2b_phase2.py — Task 54-2 phase 2: OP новых (196528, 196518) + выжимка хвоста
# (196411 union/гэпы, колизей-хвосты, ТГК) из снапов TS 0227.
import json, os, urllib.request, time, re

TS = '20261016_0227'
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

def head_text(p, n=170):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or ''
    if not t:
        t = a.get('contentHtml') or ''
    if not isinstance(t, str):
        t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

def tail_posts(fname, n=6, start=None):
    pp = sorted(posts_of(fname), key=lambda p: p.get('attributes', {}).get('number') or 0)
    for p in pp:
        a = p.get('attributes', {})
        num = a.get('number') or 0
        if start is None or num >= start:
            print(f"  #{num} {a.get('createdAt','')[:19]} :: {head_text(p)}")

for tid in (196528, 196518):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)
    print(f'\n===== OP {tid} =====')
    try:
        d = json.load(open(os.path.join(OUT, f'discussion_{tid}_near1_{TS}.json')))
        aa = d.get('data', {}).get('attributes', {})
        print(f"  title={aa.get('title')} cc={aa.get('commentCount')} createdAt={aa.get('createdAt','')[:19]}")
    except Exception as e:
        print(f'  attrs fail: {e}')
    pp = sorted(posts_of(f'discussion_{tid}_near1_{TS}.json'), key=lambda p: p.get('attributes', {}).get('number') or 0)
    for p in pp[:3]:
        a = p.get('attributes', {})
        print(f"  #{a.get('number')} {a.get('createdAt','')[:19]} :: {head_text(p, 200)}")

print('\n===== 196411 union (TS 0227) =====')
union = set()
for off in ('off0', 'off20', 'off40'):
    for p in posts_of(f'postsindex_196411_{off}_{TS}.json'):
        union.add(p.get('attributes', {}).get('number'))
for p in posts_of(f'discussion_196411_near999999_{TS}.json'):
    union.add(p.get('attributes', {}).get('number'))
nums = sorted(n for n in union if n)
gaps = sorted(set(range(1, nums[-1] + 1)) - set(nums))
print(f'union 196411 = 1..{nums[-1]}, гэпы: {gaps}')

print('\n===== 196510 tail (#19+) =====')
tail_posts(f'discussion_196510_near999999_{TS}.json', start=19)
print('\n===== 196435 tail (#136) =====')
tail_posts(f'discussion_196435_near999999_{TS}.json', start=136)

print('\n===== ТГК =====')
try:
    html = open(os.path.join(OUT, f'tg_stalzone_page0_{TS}.html'), encoding='utf-8', errors='ignore').read()
    msgs = []
    for m in re.finditer(r'data-post="stalzone/(\d+)"[\s\S]*?<time datetime="([^"]+)"[\s\S]*?(?:<div class="tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>)?[\s\S]*?(?=data-post="stalzone/|</section>)', html):
        mid, ts2, txt = m.group(1), m.group(2), m.group(3) or ''
        txt = re.sub(r'<br/?>', ' ', txt)
        txt = re.sub(r'<[^>]+>', '', txt)
        txt = re.sub(r'\s+', ' ', txt).strip()
        msgs.append((int(mid), ts2[:16], txt))
    for mid, ts2, txt in msgs[-4:]:
        print(f'  [{mid}] {ts2} :: {txt[:100]}')
except Exception as e:
    print(f'TG parse fail: {e}')
