#!/usr/bin/env python3
# emergency_rollback_refetch.py — Task 47 (инцидент): ФС откатилась к 5.10, весь canon Oct 5-14 с диска исчез.
# Пересъём критического канона: #48 sha256-сверка (canon e352e6a1... из контекста), 196428, контролы, ТГК.
import json, os, urllib.request, time, hashlib

TS = '20261014_1251'
OUT = '/home/z/my-project/output/evidence_post'
os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
CANON48 = 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e'

def get(url, name):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}'); return None
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        json.loads(body)
        print(f'OK {name} ({len(body)}B)')
        return body
    except Exception as e:
        print(f'FAIL {name}: {e}')
        return None

# 1. ГЛАВНОЕ: #48 sha256 + хвост 196411
get(f'{BASE}/api/discussions/196411?page[near]=999999', f'discussion_196411_near999999_{TS}.json'); time.sleep(1)
# 2. 196428 официальный краш-тред
get(f'{BASE}/api/discussions/196428?page[near]=999999', f'discussion_196428_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196428?page[near]=1', f'discussion_196428_near1_{TS}.json'); time.sleep(1)
# 3. OP 196411
get(f'{BASE}/api/discussions/196411?page[near]=1', f'discussion_196411_near1_{TS}.json'); time.sleep(1)
# 4. контролы
get(f'{BASE}/api/discussions/196315?page[near]=999999', f'discussion_196315_near999999_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions/196415?page[near]=999999', f'discussion_196415_near999999_{TS}.json'); time.sleep(1)
# 5. ТГК
os.system(f"curl -s -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36' 'https://t.me/s/stalzone' -o {OUT}/tg_stalzone_page0_{TS}.html && echo OK tg_stalzone")

# 6. НЕМЕДЛЕННАЯ sha256-сверка #48
f = os.path.join(OUT, f'discussion_196411_near999999_{TS}.json')
if os.path.exists(f):
    d = json.load(open(f))
    posts = [i for i in (d.get('included') or []) if i.get('type') == 'posts']
    p48 = next((p for p in posts if p.get('attributes', {}).get('number') == 48), None)
    if p48:
        a = p48['attributes']
        h = hashlib.sha256((a.get('contentHtml') or '').encode()).hexdigest()
        print(f'\n>>> #48: hiddenAt={a.get("hiddenAt")} isApproved={a.get("isApproved")} len={len(a.get("contentHtml") or "")}')
        print(f'>>> sha256 {h[:16]}... {"CANON OK ПОБАЙТОВО" if h == CANON48 else "!!! РАСХОЖДЕНИЕ С CANON"}')
    else:
        print('\n>>> #48 ОТСУТСТВУЕТ в снапе — СНОС/HIDE!')
print('REFETCH_DONE')
