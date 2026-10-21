# check54_139b_spectrum.py — межраунд 54-139b (~21:15 UTC 21.10): автор в чате:
# «прирост это другой юзер заценил новейший пост, из Интересного, это вот только что,
#  были новые "откровения" от Спектрума(есть и в ТГК тоже)» →
# (1) ТГК spectrum_zone: новые посты после 7895 (дыра 7893/7894) — сырый HTML data-post;
# (2) ТГК stalzone: новые после 3223;
# (3) фронт+витрина+/api/tags: тред/секция «Интересное» (заголовки, слаги);
# (4) Пост Санити 159759 near=14591: хвост + rx-стейт #14590 (атрибуция автора: другой юзер, НЕ прогулка).
import json, os, urllib.request, time, datetime, re

TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
BASE = 'https://forum.exbo.net'
SUM_BASE, SPEC_BASE = 3223, 7895
RES = {'TS': TS}

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

def tg_parse(fname, chan, base):
    path = os.path.join(OUT, fname)
    try:
        html = open(path, encoding='utf-8', errors='replace').read()
    except Exception as e:
        print(f'[{chan}] read fail: {e}'); return []
    ids = sorted({int(m) for m in re.findall(r'data-post="%s/(\d+)"' % chan, html)})
    print(f'[{chan}] posts_in_feed={len(ids)} min={ids[0] if ids else "-"} max={ids[-1] if ids else "-"} (baseline {base})')
    new = [i for i in ids if i > base]
    out = []
    parts = html.split('data-post="%s/' % chan)
    for p in parts[1:]:
        m = re.match(r'(\d+)', p)
        if not m: continue
        pid = int(m.group(1))
        tm = re.search(r'<time datetime="([^"]+)"', p)
        tmo = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', p, re.S)
        txt = re.sub(r'<[^>]+>', ' ', tmo.group(1)) if tmo else ''
        txt = re.sub(r'\s+', ' ', txt).strip()
        mark = ' <<< NEW' if pid > base else ''
        print(f'  {pid} @ {tm.group(1) if tm else "?"} :: {txt[:260]}{mark}')
        if pid > base:
            out.append({'id': pid, 'time': tm.group(1) if tm else None, 'text': txt[:500]})
    return out

print(f'=== INTERROUND 54-139b @ {TS} UTC ===')

# (1)+(2) ТГК
get('https://t.me/s/spectrum_zone', f'tg_spectrum_interround_{TS}.html', validate_json=False); time.sleep(1)
res_spec = tg_parse(f'tg_spectrum_interround_{TS}.html', 'spectrum_zone', SPEC_BASE)
time.sleep(1)
get('https://t.me/s/stalzone', f'tg_stalzone_interround_{TS}.html', validate_json=False); time.sleep(1)
res_sum = tg_parse(f'tg_stalzone_interround_{TS}.html', 'stalzone', SUM_BASE)

# (3) фронт + теги + поиск «Интересн»
get(f'{BASE}/api/discussions?page[offset]=0', f'frontindex_interround_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/tags', f'tags_interround_{TS}.json', validate_json=False); time.sleep(1)

def titles_of(fname):
    try:
        d = json.load(open(os.path.join(OUT, fname)))
    except Exception as e:
        print(f'PARSE FAIL {fname}: {e}'); return []
    items = []
    data = d.get('data')
    for i in (data if isinstance(data, list) else [data] if data else []):
        if isinstance(i, dict) and i.get('type') == 'discussions': items.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'discussions': items.append(i)
    return items

front = titles_of(f'frontindex_interround_{TS}.json')
print(f'\n[front] discussions={len(front)}')
inter_hits = []
for i in front:
    a = i.get('attributes', {})
    t = a.get('title') or ''
    if 'интересн' in t.lower() or 'интересн' in str(i.get('slug', '')).lower():
        inter_hits.append(i)
    print(f"  d/{i.get('id')} cc={a.get('commentCount')} last={a.get('lastPostNumber')} :: {t[:90]}")

# поиск «Интересн» в снапах прошлого раунда (0 запросов)
for old in ['tagnews_off0_20261021_2031.json', 'frontindex_off0_20261021_2031.json']:
    p = os.path.join(OUT, old)
    if not os.path.exists(p):
        # TS-варианты
        import glob as _g
        cands = sorted(_g.glob(os.path.join(OUT, old.replace('_20261021_2031', '_*'))))
        if not cands: print(f'[old] {old}: нет файла'); continue
        p = cands[-1]
    items = titles_of(os.path.basename(p))
    hits = [(i.get('id'), i.get('attributes', {}).get('title')) for i in items
            if 'интересн' in str(i.get('attributes', {}).get('title', '')).lower()]
    print(f'[old {os.path.basename(p)}] items={len(items)} интересн-hits={hits}')

# слаги тегов — искать «интересн»
try:
    tg = json.load(open(os.path.join(OUT, f'tags_interround_{TS}.json')))
    rows = tg.get('data', [])
    print(f'\n[tags] count={len(rows)}')
    for r in rows:
        a = r.get('attributes', {})
        nm = str(a.get('name', ''))
        if 'интересн' in nm.lower() or 'интересн' in str(r.get('attributes', {}).get('slug', '')).lower():
            print(f"  >>> TAG MATCH id={r.get('id')} name={nm} slug={a.get('slug')}")
    print('  slugs:', [r.get('attributes', {}).get('slug') for r in rows][:40])
except Exception as e:
    print(f'[tags] parse fail: {e}')

# (4) Пост Санити хвост: near=14591 (окно покрывает #14590 rx и свежие посты)
get(f'{BASE}/api/discussions/159759?near=14591', f'discussion_159759_near14591_interround_{TS}.json'); time.sleep(1)
try:
    d = json.load(open(os.path.join(OUT, f'discussion_159759_near14591_interround_{TS}.json')))
    aa = d.get('data', {}).get('attributes', {})
    print(f"\n[159759] cc={aa.get('commentCount')} lastPostNumber={aa.get('lastPostNumber')} locked={aa.get('isLocked')}")
    posts = []
    data = d.get('data')
    for i in (data if isinstance(data, list) else [data] if data else []):
        if isinstance(i, dict) and i.get('type') == 'posts': posts.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts': posts.append(i)
    tail = sorted(posts, key=lambda p: p.get('attributes', {}).get('number') or 0)
    for p in tail:
        a = p.get('attributes', {})
        rx = a.get('reactions') or {}
        canrx = a.get('canonicalReactions') or {}
        print(f"  #{a.get('number')} {a.get('createdAt')} likes={a.get('likes')} rx={json.dumps(rx, ensure_ascii=False)[:110]} :: {re.sub(r'<[^>]+>', ' ', str(a.get('contentPlain') or ''))[:130]}")
    RES['sanity_tail'] = [{'n': p.get('attributes', {}).get('number'), 'likes': p.get('attributes', {}).get('likes')} for p in tail]
except Exception as e:
    print(f'[159759] parse fail: {e}')

RES['spectrum_new'] = res_spec
RES['stalzone_new'] = res_sum
RES['inter_hits_front'] = [(i.get('id'), i.get('attributes', {}).get('title')) for i in inter_hits]
json.dump(RES, open(os.path.join(OUT, f'check54_139b_summary_{TS}.json'), 'w'), ensure_ascii=False, indent=1)
print(f'\nDONE interround 54-139b, TS={TS}')
