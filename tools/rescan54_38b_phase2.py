#!/usr/bin/env python3
# rescan54_38b_phase2.py — Task 54-38 phase 2: OP новых тредов окна 14:26
# (196609 «Не верю», 196610 «Раздача отс всем кроме фармящих», 196608 «Наказание в рейтинге»)
# + хвосты активировавшихся 196577 «Невидимка» (cc 13→29) и 196567 «СР3М» (+3).
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

def head_text(p, n=150):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or ''
    if not t:
        t = a.get('contentHtml') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

def show(fname, tag, tail_n=6):
    pp = posts_of(fname)
    tail = sorted(pp, key=lambda p: p.get('attributes', {}).get('number') or 0)
    if tag == 'OP':
        tail = tail[:1]
    else:
        tail = tail[-tail_n:]
    for p in tail:
        a = p.get('attributes', {})
        print(f"  #{a.get('number')} {a.get('createdAt','')[:19]} :: {head_text(p)}")

print('=== NEW OPs (near=1) ===')
for tid, label in ((196609, 'Не верю'), (196610, 'Раздача ОТС не-фармерам'), (196608, 'Наказание в рейтинге')):
    fn = f'discussion_{tid}_near1_{TS}.json'
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', fn); time.sleep(1)
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        aa = d.get('data', {}).get('attributes', {})
        print(f'[{tid}] «{label}» cc={aa.get("commentCount")} createdAt={aa.get("createdAt","")[:16]}')
        show(fn, 'OP')
    except Exception as e:
        print(f'[{tid}] meta fail {e}')

print('\n=== активировавшиеся хвосты (near=999999) ===')
for tid, label in ((196577, 'Невидимка'), (196567, 'СР3М')):
    fn = f'discussion_{tid}_near999999_{TS}.json'
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', fn); time.sleep(1)
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        aa = d.get('data', {}).get('attributes', {})
        print(f'[{tid}] «{label}» cc={aa.get("commentCount")} LPN={aa.get("lastPostNumber")}')
        show(fn, 'TAIL')
    except Exception as e:
        print(f'[{tid}] meta fail {e}')

print(f'\nTS={TS}')
