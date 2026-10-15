#!/usr/bin/env python3
# rescan54_20b_phase2.py — добор OP новых тредов 196511/196469 + текст ТГК 3204 (без повторных GET по ключам)
import json, os, urllib.request, time, datetime, re, hashlib

TS = '20261015_2010'   # фаза 1 (файлы витрин/тредов)
TS2 = '20261015_2012'  # фаза 2 (OP-добор 196511/196469)
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

# === OP-добор новых тредов фронта ===
for tid in (196511, 196469):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS2}.json'); time.sleep(1)

# === 1. Что за 196511 и 196469 (из frontindex) ===
for fn in (f'frontindex_off0_{TS}.json',):
    try:
        d = json.load(open(os.path.join(OUT, fn)))
        for i in d.get('data', []):
            if i.get('id') in ('196511', '196469'):
                a = i.get('attributes', {})
                print(f"FRONT [{i.get('id')}] {a.get('title')} | createdAt={a.get('createdAt')} lastPostedAt={a.get('lastPostedAt')} cc={a.get('commentCount')}")
    except Exception as e:
        print(f'front parse fail {e}')

# === 2. OP + хвост 196511/196469 ===
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

def head_text(p, n=200):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or a.get('contentHtml') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

for tid in (196511, 196469):
    fn = f'discussion_{tid}_near1_{TS2}.json'
    try:
        dd = json.load(open(os.path.join(OUT, fn)))
        aa = dd.get('data', {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
        print(f"\n[{tid}] cc={aa.get('commentCount')} LPN={aa.get('lastPostNumber')} :: {aa.get('title','')}")
        pp = sorted(posts_of(fn), key=lambda p: p.get('attributes', {}).get('number') or 0)
        for p in pp[:3]:
            a = p.get('attributes', {})
            lim = 1200 if tid == 196511 else 200
            print(f"  #{a.get('number')} {a.get('createdAt')} :: {head_text(p, lim)}")
    except Exception as e:
        print(f'[{tid}] fail {e}')

# === 3. ТГК 3204 текст из уже скачанного HTML ===
html_path = os.path.join(OUT, f'tg_stalzone_page0_{TS}.html')
html = open(html_path, encoding='utf-8', errors='ignore').read()
m = re.search(r'data-post="stalzone/3204"[\s\S]*?(?=data-post="stalzone/|</section>)', html)
if m:
    block = m.group(0)
    mt = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>', block)
    txt = mt.group(1) if mt else '(нет текстового блока — фото/видео?)'
    txt = re.sub(r'<br/?>', ' | ', txt)
    txt = re.sub(r'<[^>]+>', '', txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    print(f'\nТГК 3204: {txt[:500]}')
    # реакции
    for rr in re.finditer(r'<span class="tgme_widget_message_reaction[^"]*"[^>]*>([\s\S]*?)</span>', block):
        print('  реакция:', re.sub(r'<[^>]+>', '', rr.group(1)).strip()[:40])
else:
    print('ТГК 3204 не найден в HTML')

# === 4. #48 канон по postsindex (sha256 от contentHtml) ===
for off in ('off0', 'off20', 'off40'):
    fn = os.path.join(OUT, f'postsindex_196411_{off}_{TS}.json')
    try:
        d = json.load(open(fn))
        for i in (d.get('data') or []) + (d.get('included') or []):
            if isinstance(i, dict) and i.get('type') == 'posts' and i.get('attributes', {}).get('number') == 48:
                h = hashlib.sha256((i['attributes'].get('contentHtml') or '').encode()).hexdigest()
                print(f"\n#48 (postsindex {off}): sha256={h[:16]}... {'CANON OK' if h == CANON48 else '!!! ИЗМЕНИЛСЯ'} rx={sum((i['attributes'].get('reactionCounts') or {}).values())}")
    except Exception as e:
        print(f'#48 {off} fail: {e}')

# === 5. Дыры в ОТС 196424 (LPN=90, cc=88) ===
fn = os.path.join(OUT, f'discussion_196424_near999999_{TS}.json')
pp = posts_of(fn)
nums = sorted((p.get('attributes', {}).get('number') or 0) for p in pp)
full = set(range(1, (nums[-1] if nums else 0) + 1))
print(f'\nОТС 196424: покрыто near-окном {nums[0] if nums else 0}..{nums[-1] if nums else 0}, дыры в окне: {sorted(full - set(nums))}')

# === 6. Дыры в 196461 (LPN=153, cc=150) ===
fn = os.path.join(OUT, f'discussion_196461_near999999_{TS}.json')
pp = posts_of(fn)
nums = sorted((p.get('attributes', {}).get('number') or 0) for p in pp)
full = set(range(1, (nums[-1] if nums else 0) + 1))
print(f'196461 ттк: покрыто {nums[0] if nums else 0}..{nums[-1] if nums else 0}, дыры в окне: {sorted(full - set(nums))}')

print(f'\nTS_phase2={TS}')
