# rescan54_127_phase2.py — OP-фetch для NEW front 54-127: 196772/196782/196781
import json, os, urllib.request, time, re

TS = '0831'
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

def head_text(p, n=130):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or ''
    if not isinstance(t, str):
        t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

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

for tid in (196772, 196782, 196781):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)
    for near in ('near1', 'near999999'):
        fn = f'discussion_{tid}_{near}_{TS}.json'
        try:
            dd = json.load(open(os.path.join(OUT, fn)))
            aa = dd.get('data', {}).get('attributes', {})
            print(f'[{tid}/{near}] title={aa.get("title","?")[:70]} cc={aa.get("commentCount")} LPN={aa.get("lastPostNumber")} createdAt={str(aa.get("createdAt"))[:16]}')
            pp = sorted(posts_of(fn), key=lambda p: p.get('attributes', {}).get('number') or 0)
            for p in (pp[:2] if near == 'near1' else pp[-3:]):
                a = p.get('attributes', {})
                print(f'  #{a.get("number")} {str(a.get("createdAt"))[:16]} :: {head_text(p)}')
        except Exception as e:
            print(f'[{tid}/{near}] fail: {e}')
print('PHASE2 DONE')
