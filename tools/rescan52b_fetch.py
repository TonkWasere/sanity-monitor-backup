#!/usr/bin/env python3
# rescan52b_fetch.py — Task 52 фаза 2: точечные докачки (Передовой кейс 196488/196480/196452, аутентификатор 196283, postsindex 196411 верификация #48/#51/#54/#56) TS (auto UTC).
import json, os, urllib.request, time, datetime

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

# 1) Передовой кейс: новый баг-тред + дискуссионный + тред про посылки
get(f'{BASE}/api/discussions/196488?page[near]=1', f'discussion_196488_near1_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196488?page[near]=999999', f'discussion_196488_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196480?page[near]=1', f'discussion_196480_near1_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196480?page[near]=999999', f'discussion_196480_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196452?page[near]=1', f'discussion_196452_near1_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196452?page[near]=999999', f'discussion_196452_near999999_{TS}.json'); time.sleep(1)
# 2) Аутентификатор (cc=82, хвост)
get(f'{BASE}/api/discussions/196283?page[near]=999999', f'discussion_196283_near999999_{TS}.json'); time.sleep(1)
# 3) 196411 postsindex верификация судьбы #48/#51/#54/#56 (окна 0/20/40)
get(f'{BASE}/api/posts?filter%5Bdiscussion%5D=196411&page%5Bsize%5D=20&page%5Boffset%5D=0', f'postsindex_196411_off0_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/posts?filter%5Bdiscussion%5D=196411&page%5Bsize%5D=20&page%5Boffset%5D=20', f'postsindex_196411_off20_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/posts?filter%5Bdiscussion%5D=196411&page%5Bsize%5D=20&page%5Boffset%5D=40', f'postsindex_196411_off40_{TS}.json'); time.sleep(1)
print(f'TS={TS}')
