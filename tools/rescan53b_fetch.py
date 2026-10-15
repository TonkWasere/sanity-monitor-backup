#!/usr/bin/env python3
# rescan53b_fetch.py — Task 53 дозабор: OP 196424 (Тестовый Сервер 16.10), OP 196490 (конкурс),
# OP 196411 (edited?), ТГК 3202/3203 — реакции/тексты через getLikes Counter / сырой html.
import json, os, urllib.request, time, datetime, re, html as ihtml

TS = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M')
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

for tid in (196424, 196490, 196411):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)

# реакции по новым постам 196411 (#75-79) и 196488 (#44-48) — из уже скачанных near999999
print('\n===== РЕАКЦИИ ХВОСТОВ =====')
for tid, nums in ((196411, [75, 76, 77, 78, 79]), (196488, [44, 45, 46, 47, 48]), (196452, [16, 17, 18, 19, 20])):
    try:
        d = json.load(open(os.path.join(OUT, f'discussion_{tid}_near999999_{TS}.json')))
        items = d.get('data') if isinstance(d.get('data'), list) else []
        items += d.get('included') or []
        for p in items:
            if isinstance(p, dict) and p.get('type') == 'posts' and p.get('attributes', {}).get('number') in nums:
                a = p['attributes']
                rc = a.get('reactionCounts') or {}
                print(f"  [{tid} #{a['number']}] {a.get('createdAt','')[:16]} rx={rc} likes={a.get('likesCount')} :: {(a.get('contentPlain') or '')[:90]}")
    except Exception as e:
        print(f'{tid} fail: {e}')

# ТГК 3202/3203: текст + реакции из свежего html
print('\n===== ТГК 3199-3203 детали =====')
try:
    raw = open(os.path.join(OUT, f'tg_stalzone_page0_{TS}.html'), encoding='utf-8', errors='ignore').read()
    # разбиваем по сообщениям
    parts = re.split(r'(?=<div class="tgme_widget_message )', raw)
    for part in parts:
        m = re.search(r'data-post="stalzone/(\d+)"', part)
        if not m:
            continue
        mid = int(m.group(1))
        if mid < 3199:
            continue
        tm = re.search(r'<time datetime="([^"]+)"', part)
        ts = tm.group(1)[:16] if tm else '?'
        tmx = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>', part)
        txt = ''
        if tmx:
            txt = re.sub(r'<br/?>', ' | ', tmx.group(1))
            txt = re.sub(r'<[^>]+>', '', txt)
            txt = ihtml.unescape(re.sub(r'\s+', ' ', txt)).strip()
        views = re.search(r'tgme_widget_message_views[^>]*>([\d.,KKM]+)', part)
        likes = re.search(r'tgme_widget_message_like[^>]*>([\d.,KKM]+)', part) or re.search(r'data-reaction="🫡"[^>]*>([\d.,KKM]+)', part)
        # реакции: tgme_widget_message_reactions блоки
        reacts = re.findall(r'class="tgme_widget_message_reaction[^"]*"[^>]*>\s*<i class="emoji"[^>]*>([^<]+)</i>\s*<span[^>]*>([\d.,KKM]+)', part)
        disl = re.findall(r'data-reaction="([^"]+)"[^>]*>\s*<span[^>]*>([\d.,KKM]+)', part)
        print(f'  [{mid}] {ts} views={views.group(1) if views else "?"} :: {txt[:180]}')
        if reacts or disl:
            print(f'      reactions: {reacts} {disl}')
except Exception as e:
    print(f'TG detail fail: {e}')

print(f'\nTS={TS}')
