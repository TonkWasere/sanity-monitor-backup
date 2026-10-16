#!/usr/bin/env python3
# rescan49_fetch.py — Task 49: верификационный проход «погуляла ли модерация» TS (auto UTC).
import json, os, urllib.request, time, hashlib, datetime

TS = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
CANON48 = 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e'

def get(url, name):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}'); return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        json.loads(body)
        print(f'OK {name} ({len(body)}B)')
        return True
    except Exception as e:
        print(f'FAIL {name}: {e}')
        return False

get(f'{BASE}/api/discussions/196411?page[near]=999999', f'discussion_196411_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196411?page[near]=1', f'discussion_196411_near1_{TS}.json'); time.sleep(1)
for off in (0, 20, 40, 60):
    get(f'{BASE}/api/posts?filter[discussion]=196411&page[offset]={off}&page[limit]=20',
        f'postsindex_196411_off{off}_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196428?page[near]=999999', f'discussion_196428_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196315?page[near]=999999', f'discussion_196315_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196415?page[near]=999999', f'discussion_196415_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions?page[offset]=0', f'frontindex_off0_{TS}.json'); time.sleep(1)
get('https://t.me/s/stalzone', f'tg_stalzone_page0_{TS}.html')

# немедленная сверка #48
d = json.load(open(os.path.join(OUT, f'discussion_196411_near999999_{TS}.json')))
posts = [i for i in (d.get('included') or []) if i.get('type') == 'posts']
p48 = next((p for p in posts if p.get('attributes', {}).get('number') == 48), None)
if not p48:
    print('\n>>> #48 ОТСУТСТВУЕТ — СНОС/HIDE!')
else:
    a = p48['attributes']
    h = hashlib.sha256((a.get('contentHtml') or '').encode()).hexdigest()
    print(f"\n>>> #48: sha256 {h[:16]}... {'CANON OK' if h == CANON48 else '!!! ИЗМЕНИЛСЯ'} hiddenAt={a.get('hiddenAt')} isApproved={a.get('isApproved')} rx={sum((a.get('reactionCounts') or {}).values())} likes={a.get('likesCount')}")
print(f'TS={TS}')
