#!/usr/bin/env python3
# rescan54_75b_phase2.py — Task 54-75: OP нового треда окна 03:29 UTC (196677) near1+near999999,
# + свежие хвосты ночных линий 196626 (соло 172→?), 196661 (покровник 44→?), 196670 (10→?).
import json, os, time, urllib.request

BASE = 'https://forum.exbo.net'
OUT = '/home/z/my-project/output/evidence_post'
TS = "20261019_0331"
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')

def get(url, fname):
    dst = os.path.join(OUT, fname)
    if os.path.exists(dst):
        print('SKIP', fname); return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        open(dst, 'wb').write(data)
        if fname.endswith('.json'):
            json.loads(data.decode('utf-8'))  # валидация
        print('OK', fname, f'({len(data)}B)'); time.sleep(1); return True
    except Exception as e:
        print('FAIL', fname, e); return False

# --- OP нового треда окна (проверка createdAt обязательна) ---
for tid in (196677,):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json')
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json')
# --- хвосты ночных линий на момент снапшота ---
for tid in (196626, 196661, 196670, 196673, 196501):
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json')
print('done')
