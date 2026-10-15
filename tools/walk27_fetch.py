#!/usr/bin/env python3
# walk27_fetch.py — снапшоты обхода №27 (Task 40), TS 20261014_0940
# Зеркало набора №26 (Task 39) + search_patch + search_sobytie.
import json, os, urllib.request, urllib.parse, time, sys

TS = '20261014_0940'
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
        # sanity: json должен парситься (не Cloudflare-заглушка)
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

# 1. frontindex
get(f'{BASE}/api/discussions?page[offset]=0', f'frontindex_off0_{TS}.json')
time.sleep(1)

# 2. дельты near999999 ×13
for tid in (195574, 195660, 196033, 195889, 196062, 196074, 196078, 194423, 196180, 196276, 196283, 196315, 196326):
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json')
    time.sleep(1)

# 3. near1-окна
for tid in (195660, 196341, 196380, 196411):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json')
    time.sleep(1)
# 196341 + 196411 хвосты
get(f'{BASE}/api/discussions/196341?page[near]=999999', f'discussion_196341_near999999_{TS}.json')
time.sleep(1)
get(f'{BASE}/api/discussions/196411?page[near]=999999', f'discussion_196411_near999999_{TS}.json')
time.sleep(1)

# 4. точечные окна
get(f'{BASE}/api/discussions/51716?page[near]=524', f'discussion_51716_near524_{TS}.json')
time.sleep(1)
get(f'{BASE}/api/discussions/188595?page[near]=9', f'discussion_188595_near9_{TS}.json')
time.sleep(1)

# 5. postsindex (метод №26.1)
for tid, offs in ((195660, [0, 50, 100, 150, 200, 250, 300, 350, 400]),
                  (196276, [0]), (196283, [0, 50]), (196315, [0, 50]),
                  (196326, [0]), (196341, [0, 50]), (196411, [0, 50])):
    for off in offs:
        get(f'{BASE}/api/posts?filter[discussion]={tid}&page[offset]={off}&page[limit]=50',
            f'postsindex_{tid}_off{off}_{TS}.json')
        time.sleep(1)

# 6. поиски
get(f"{BASE}/api/discussions?filter[q]=" + urllib.parse.quote('Неизбежность'), f'search_neizbezhnost_{TS}.json')
time.sleep(1)
get(f"{BASE}/api/discussions?filter[q]=" + urllib.parse.quote('патч'), f'search_patch_{TS}.json')
time.sleep(1)
get(f"{BASE}/api/discussions?filter[q]=" + urllib.parse.quote('событие'), f'search_sobytie_{TS}.json')
time.sleep(1)

# 7. ТГК page0
get('https://t.me/s/stalzone', f'tg_stalzone_page0_{TS}.html')
time.sleep(1)
get('https://t.me/s/spectrum_zone', f'tg_spectrum_zone_page0_{TS}.html')

print(f'\nDONE: ok={done} fail={fail}')
