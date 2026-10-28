#!/usr/bin/env python3
# rescan46_fetch.py — Task 46: ОФИЦИАЛЬНЫЙ ТГК stalzone запостил про краши (лаг ~30 мин от юзер-свидетельств).
# Перехват поста + судьба #48 + официальный форумный след. TS 20261014_1148 (UTC).
import json, os, urllib.request, urllib.parse, time

TS = '20261014_1148'
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

# 1. ТГК — перехват официального поста (stalzone + spectrum)
get('https://t.me/s/stalzone', f'tg_stalzone_page0_{TS}.html')
time.sleep(1)
get('https://t.me/s/spectrum_zone', f'tg_spectrum_zone_page0_{TS}.html')
time.sleep(1)

# 2. Судьба #48 + официальный форумный след
get(f'{BASE}/api/discussions/196411?page[near]=999999', f'discussion_196411_near999999_{TS}.json')
time.sleep(1)
get(f'{BASE}/api/discussions?page[offset]=0', f'frontindex_off0_{TS}.json')
time.sleep(1)

# 3. Поиски: краш/ошибка — новые юзер-треды + официальный
get(f"{BASE}/api/discussions?filter[q]=" + urllib.parse.quote('краш'), f'search_krash_{TS}.json')
time.sleep(1)
get(f"{BASE}/api/discussions?filter[q]=" + urllib.parse.quote('вылетает'), f'search_vyletaet_{TS}.json')
time.sleep(1)

# 4. postsindex хвоста 196411 (off40 — номера 41+)
get(f'{BASE}/api/posts?filter[discussion]=196411&page[offset]=40&page[limit]=20', f'postsindex_196411_off40_{TS}.json')

print(f'\nDONE: ok={done} fail={fail}')
