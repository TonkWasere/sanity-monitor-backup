#!/usr/bin/env python3
# rescan54_33b_phase2.py — Task 54-33: OP NEW 196593 + хвосты моверов 196573/168572/196475.
import json, os, urllib.request, time, datetime, re

TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'

def get(url, name):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}'); return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
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

def head_text(p, n=130):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or a.get('contentHtml') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

def summary(tid, head_n=5, tail_n=6):
    fn = f'discussion_{tid}_near999999_{TS}.json'
    pp = posts_of(fn)
    try:
        dd = json.load(open(os.path.join(OUT, fn)))
        aa = dd.get('data', {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
        print(f"[{tid}] cc={aa.get('commentCount')} lastPostNumber={aa.get('lastPostNumber')} title={aa.get('title','')!r} createdAt={str(aa.get('createdAt',''))[:16]} user={ (dd.get('included') or [{}])[0].get('attributes',{}).get('username','?') if isinstance(dd.get('included'), list) and dd.get('included') else '?'}")
    except Exception as e:
        print(f'[{tid}] attrs fail {e}')
    allp = sorted(pp, key=lambda p: p.get('attributes', {}).get('number') or 0)
    for p in allp[:head_n]:
        a = p.get('attributes', {})
        print(f"  OP#{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")
    for p in allp[-tail_n:]:
        a = p.get('attributes', {})
        print(f"  #{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")

# NEW 196593 «сборки» — OP обязателен
get(f'{BASE}/api/discussions/196593?page[near]=1', f'discussion_196593_near1_{TS}.json'); time.sleep(1)
summary(196593)
# хвосты моверов
for tid in (196573, 168572, 196475):
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)
    summary(tid, head_n=0)

print(f'TS={TS}')
