#!/usr/bin/env python3
# rescan54_22b_phase2.py — OP 196516/196510 + верификация сноса #70 в 196411 + хвост Crios-ответов 196435
import json, os, urllib.request, time, re, datetime

TS = '20261015_2209'
TS2 = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
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
    out = []
    for i in (d.get('data') if isinstance(d.get('data'), list) else []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    return out

def head_text(p, n=230):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or a.get('contentHtml') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

# === OP-добор ===
for tid in (196516, 196510):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS2}.json'); time.sleep(1)

for tid in (196516, 196510):
    fn = f'discussion_{tid}_near1_{TS2}.json'
    try:
        dd = json.load(open(os.path.join(OUT, fn)))
        aa = dd.get('data', {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
        print(f"\n[{tid}] cc={aa.get('commentCount')} LPN={aa.get('lastPostNumber')} createdAt={aa.get('createdAt')} :: {aa.get('title','')}")
        pp = sorted(posts_of(fn), key=lambda p: p.get('attributes', {}).get('number') or 0)
        for p in pp[:2]:
            a = p.get('attributes', {})
            print(f"  #{a.get('number')} {a.get('createdAt')} :: {head_text(p)}")
    except Exception as e:
        print(f'[{tid}] fail {e}')

# === Верификация сноса #70 (196411, фаза 1) ===
fn = os.path.join(OUT, f'discussion_196411_near999999_{TS}.json')
pp = posts_of(fn)
nums = sorted((p.get('attributes', {}).get('number') or 0) for p in pp)
print(f'\n196411 near999999 покрытие: {nums[0]}..{nums[-1]} ({len(nums)} шт)')
print(f'>>> #70 в покрытии? {"НЕТ — СНОС ПОДТВЕРЖДЁН" if 70 not in nums else "да — жив"}')

# === Crios-ответы в 196435 (полный текст #132-133) ===
fn = os.path.join(OUT, f'discussion_196435_near999999_{TS}.json')
try:
    d = json.load(open(os.path.join(OUT, fn)))
    dd = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
    print(f"\n196435 attrs: cc={dd.get('commentCount')} LPN={dd.get('lastPostNumber')} createdAt={dd.get('createdAt')}")
    for p in posts_of(fn):
        a = p.get('attributes', {})
        if a.get('number') in (130, 131, 132, 133, 134):
            print(f"  #{a.get('number')} {a.get('createdAt')} :: {head_text(p, 300)}")
except Exception as e:
    print(f'196435 fail {e}')

print(f'\nTS_phase2={TS2}')
