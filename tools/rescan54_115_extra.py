#!/usr/bin/env python3
# rescan54_115_extra.py — добор: 196757 (выпал из хвостов в 54-114) + 196369 near1 (не в KNOWN).
import json, os, urllib.request, time, datetime

TS = '20261020_1950'
OUT = '/home/z/my-project/output/evidence_post'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

def get(url, dst):
    if os.path.exists(dst):
        print('SKIP', dst); return True
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        body = urllib.request.urlopen(req, timeout=30).read()
    except Exception as e:
        print(f'FAIL {dst}: {e}'); return False
    try:
        json.loads(body.decode('utf-8'))
    except Exception as e:
        print(f'PARSE FAIL {dst}: {e}'); return False
    open(dst, 'wb').write(body)
    print(f'OK {dst} ({len(body)}B)')
    return True

BASE = 'https://forum.exbo.net/api/discussions'
get(f'{BASE}/196757?sort=-lastPostedAt&page[near]=999999', f'{OUT}/discussion_196757_near999999_{TS}.json')
time.sleep(1)
get(f'{BASE}/196369?sort=-lastPostedAt&page[near]=1', f'{OUT}/discussion_196369_near1_{TS}.json')
time.sleep(1)

for tid, near in ((196757, '999999'), (196369, '1')):
    try:
        d = json.load(open(f'{OUT}/discussion_{tid}_near{near}_{TS}.json'))
        a = d.get('data', {}).get('attributes', {})
        print(f"[{tid}] «{a.get('title','')}» createdAt={str(a.get('createdAt'))[:16]} cc={a.get('commentCount')} LPN={a.get('lastPostNumber')} locked={a.get('isLocked')}")
        posts = d.get('included') or []
        for p in posts[-6:]:
            pa = p.get('attributes', {})
            print('  #' + str(pa.get('number')), str(pa.get('createdAt'))[:16], '::', (pa.get('content') or '')[:90])
    except Exception as e:
        print(f'[{tid}] read fail: {e}')
print('TS=' + TS)
