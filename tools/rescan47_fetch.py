#!/usr/bin/env python3
# rescan47_fetch.py — Task 47: восстановление после отката ВМ + дожим раунда TS 20261014_1253.
# Пересъём union-карты 196411, медиа ТГК 3197, frontindex, search_patch, html_preload.
import json, os, re, urllib.request, time, hashlib

TS = '20261014_1253'
OUT = '/home/z/my-project/output/evidence_post'
os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}

done = fail = 0
def get(url, name, binary=False):
    global done, fail
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}'); done += 1; return None
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        if not binary:
            json.loads(body)
        print(f'OK {name} ({len(body)}B)')
        done += 1
        return body
    except Exception as e:
        print(f'FAIL {name}: {type(e).__name__}: {e}')
        fail += 1
        return None

# 1. union-карта 196411
for off in (0, 20, 40, 60):
    get(f'https://forum.exbo.net/api/posts?filter[discussion]=196411&page[offset]={off}&page[limit]=20',
        f'postsindex_196411_off{off}_{TS}.json')
    time.sleep(1)

# 2. frontindex + search_patch
get('https://forum.exbo.net/api/discussions?page[offset]=0', f'frontindex_off0_{TS}.json'); time.sleep(1)
get('https://forum.exbo.net/api/discussions?filter[q]=' + urllib.parse.quote('патч'), f'search_patch_{TS}.json'); time.sleep(1)

# 3. html_preload 196411 (гостевой вид)
get('https://forum.exbo.net/d/196411-igrovye-izmeneniya-vstupili-v-silu',
    f'html_preload_196411-igrovye-izmeneniya-vstupili-v-silu_{TS}.html', binary=True); time.sleep(1)

# 4. медиа ТГК 3197 — парсим URL из свежего HTML (1251) и бэкапим
html_p = os.path.join(OUT, 'tg_stalzone_page0_20261014_1251.html')
if os.path.exists(html_p):
    s = open(html_p, encoding='utf-8').read()
    m3197 = re.search(r'data-post="stalzone/3197"(.*?)(?=data-post="stalzone/3198"|class="tgme_widget_message_divider|$)', s, re.S)
    if m3197:
        blk = m3197.group(1)
        urls = re.findall(r"https://cdn\d+\.telesco\.pe/file/[^\"']+", blk)
        seen = set()
        for i, u in enumerate(urls):
            if u in seen: continue
            seen.add(u)
            get(u, f'tg3197_media{i+1}_{TS}.jpg', binary=True)
            time.sleep(1)
    else:
        print('!! блок 3197 не найден в HTML')

print(f'\nDONE: ok={done} fail={fail}')
