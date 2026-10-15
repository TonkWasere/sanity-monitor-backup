#!/usr/bin/env python3
# rescan46c_fetch.py — Task 46 (продолжение): экстренный обход TS 20261014_1243 «ловим пока висят».
# [РЕКОНСТРУКЦИЯ из контекста сессии Task 47 — оригинал утрачен при откате ВМ 12:48 UTC; файлы TS 1243 тоже утрачены,
#  данные сохранены в monitoring/RECOVERY_20261014_rollback.md; повторный запуск создаст TS-дубли — skip-if-exists защищает]
import json, os, urllib.request, time

TS = '20261014_1243'
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
            json.loads(body)
        print(f'OK {name} ({len(body)}B)')
        done += 1
    except Exception as e:
        print(f'FAIL {name}: {type(e).__name__}: {e}')
        fail += 1

get(f'{BASE}/api/discussions/196411?page[near]=999999', f'discussion_196411_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196428?page[near]=999999', f'discussion_196428_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196428?page[near]=1', f'discussion_196428_near1_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196411?page[near]=1', f'discussion_196411_near1_{TS}.json'); time.sleep(1)
for off in (0, 20, 40, 60):
    get(f'{BASE}/api/posts?filter[discussion]=196411&page[offset]={off}&page[limit]=20',
        f'postsindex_196411_off{off}_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196315?page[near]=999999', f'discussion_196315_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196415?page[near]=999999', f'discussion_196415_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions?page[offset]=0', f'frontindex_off0_{TS}.json'); time.sleep(1)
get('https://t.me/s/stalzone', f'tg_stalzone_page0_{TS}.html'); time.sleep(1)
get(f'{BASE}/d/196411-igrovye-izmeneniya-vstupili-v-silu', f'html_preload_196411-igrovye-izmeneniya-vstupili-v-silu_{TS}.html')
print(f'\nDONE: ok={done} fail={fail}')
