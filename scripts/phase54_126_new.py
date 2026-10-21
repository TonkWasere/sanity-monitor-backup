#!/usr/bin/env python3
# phase54_126_new.py — Task 54-126: фаза-2 — OP новых тредов окна 05:27-07:28
# (196777 «Тирлист оружий против пакеров» cc=23, 196773 «Минутка доброты!» cc=11)
# near1 (OP) + near999999 (атрибуты/хвост) — образец tools/rescan54_22b_phase2.py
import json, os, re, time, urllib.request

BASE = 'https://forum.exbo.net'
OUT = '/home/z/my-project/output/evidence_post'
TS = '0731'
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')

def get(url, fname):
    dst = os.path.join(OUT, fname)
    if os.path.exists(dst):
        print('SKIP', fname); return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        open(dst, 'wb').write(data)
        json.loads(data)
        print('OK', fname, f'({len(data)}B)'); time.sleep(1); return True
    except Exception as e:
        print('FAIL', fname, e); return False

def head_text(p, n=300):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or a.get('contentHtml') or ''
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()[:n]

for tid in (196777, 196773):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)
    for near in ('1', '999999'):
        fn = os.path.join(OUT, f'discussion_{tid}_near{near}_{TS}.json')
        try:
            d = json.load(open(fn))
            aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
            posts = [i for i in (d.get('data') if isinstance(d.get('data'), list) else []) + (d.get('included') or [])
                     if isinstance(i, dict) and i.get('type') == 'posts']
            print(f'[{tid} near{near}] title={aa.get("title","?")!r} cc={aa.get("commentCount")} LPN={aa.get("lastPostNumber")} createdAt={str(aa.get("createdAt"))[:16]} user={aa.get("user",{}).get("username") if isinstance(aa.get("user"),dict) else "?"}')
            for p in (posts[:1] if near == '1' else sorted(posts, key=lambda p: p.get('attributes', {}).get('number') or 0)[-5:]):
                a = p.get('attributes', {})
                print(f'  #{a.get("number")} {str(a.get("createdAt"))[:16]} :: {head_text(p)}')
        except Exception as e:
            print(f'[{tid} near{near}] parse fail: {e}')
print('PHASE2 DONE')
