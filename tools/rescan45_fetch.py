#!/usr/bin/env python3
# rescan45_fetch.py — Task 45: автор запостил фулл-пост от PatronOfSanity в d/196411 (ответ на #28).
# Приоритет: перехват поста в свежем снапе (риск hide/сноса — прецеденты #389/#415, #15/#33 в 196411).
# TS 20261014_1144 (UTC). Протокол: UA Chrome, sleep 1s, skip-if-exists, JSON-валидация.
import json, os, urllib.request, urllib.parse, time

TS = '20261014_1144'
OUT = '/home/z/my-project/output/evidence_post'
os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'

done = fail = 0

def get(url, name):
    global done, fail
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP (exists) {name}')
        done += 1
        return
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        with open(path, 'wb') as f:
            f.write(body)
        if name.endswith('.json'):
            try:
                json.loads(body)
            except Exception:
                print(f'!! NON-JSON {name} ({len(body)}B) — удаляю')
                os.remove(path)
                fail += 1
                return
        print(f'OK {name} ({len(body)}B)')
        done += 1
    except Exception as e:
        print(f'FAIL {name}: {type(e).__name__}: {e}')
        fail += 1

# 1. ГЛАВНОЕ: хвост 196411 — там пост Санити
get(f'{BASE}/api/discussions/196411?page[near]=999999', f'discussion_196411_near999999_{TS}.json')
time.sleep(1)
get(f'{BASE}/api/discussions/196411?page[near]=1', f'discussion_196411_near1_{TS}.json')
time.sleep(1)

# 2. postsindex 196411 (union-карта; pageSize=20 — факт №44)
for off in (0, 20, 40, 60):
    get(f'{BASE}/api/posts?filter[discussion]=196411&page[offset]={off}&page[limit]=20',
        f'postsindex_196411_off{off}_{TS}.json')
    time.sleep(1)

# 3. контролы тихих запретов
get(f'{BASE}/api/discussions/196315?page[near]=999999', f'discussion_196315_near999999_{TS}.json')
time.sleep(1)
get(f'{BASE}/api/discussions/196415?page[near]=999999', f'discussion_196415_near999999_{TS}.json')
time.sleep(1)

# 4. frontindex + search_patch (×5 верификация отсутствия «Патчноут [14.10.2026]»)
get(f'{BASE}/api/discussions?page[offset]=0', f'frontindex_off0_{TS}.json')
time.sleep(1)
get(f"{BASE}/api/discussions?filter[q]=" + urllib.parse.quote('патч'), f'search_patch_{TS}.json')
time.sleep(1)

# 5. ТГК stalzone (дельты 3196)
get('https://t.me/s/stalzone', f'tg_stalzone_page0_{TS}.html')
time.sleep(1)

# 6. HTML-прейлоад 196411 (гостевой вид)
get(f'{BASE}/d/196411-igrovye-izmeneniya-vstupili-v-silu', f'html_preload_196411-igrovye-izmeneniya-vstupili-v-silu_{TS}.html')

print(f'\nDONE: ok={done} fail={fail}')
