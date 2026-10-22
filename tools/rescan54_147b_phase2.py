# rescan54_147b_phase2.py — фаза-2: OP NEW 196802 (near1+near999999) + снапы-доборы по дельтам
import json, os, urllib.request, time

TS = '20261022_0430'
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

# NEW 196802: near1 (OP) + near999999 (хвост) — ОБА по правилу
get(f'{BASE}/api/discussions/196802?page%5Bnear%5D=1', f'discussion_196802_near1_{TS}.json')
get(f'{BASE}/api/discussions/196802?page%5Bnear%5D=999999', f'discussion_196802_near999999_{TS}.json')

# доборы: дельт-треды, где нужны авторства хвоста
get(f'{BASE}/api/discussions/196810?page%5Bnear%5D=999999', f'discussion_196810_near999999_{TS}.json', True)
get(f'{BASE}/api/discussions/196778?page%5Bnear%5D=999999', f'discussion_196778_near999999_{TS}.json', True)
print('PHASE2 FETCH DONE')
