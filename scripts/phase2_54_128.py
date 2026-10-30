#!/usr/bin/env python3
# phase2_54_128.py — OP-слепки для 6 NEW фронт-тредов раунда 54-128 (near=1 + near999999)
import json, os, time, urllib.request, datetime

BASE = 'https://forum.exbo.net'
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'}
TS = datetime.datetime.now(datetime.UTC).strftime('%Y%m%d_%H%M')
NEW = [196778, 196785, 196783, 196786, 196787, 196784]

def get(url, name):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}')
        return True
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

for tid in NEW:
    for near in ('1', '999999'):
        get(f'{BASE}/api/discussions/{tid}?page[near]={near}', f'discussion_{tid}_near{near}_{TS}.json')
        time.sleep(1)
print(f'PHASE2 TS={TS} DONE')
