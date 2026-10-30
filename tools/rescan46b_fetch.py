#!/usr/bin/env python3
# rescan46b_fetch.py — Task 46-добор: официальный тред 196428 (краши) + медиа-бекап ТГК 3197.
import json, os, urllib.request, time, hashlib

TS = '20261014_1215'
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

# 1. Официальный тред крашей: голова + хвост + индекс
get(f'{BASE}/api/discussions/196428?page[near]=1', f'discussion_196428_near1_{TS}.json')
time.sleep(1)
get(f'{BASE}/api/discussions/196428?page[near]=999999', f'discussion_196428_near999999_{TS}.json')
time.sleep(1)
get(f'{BASE}/api/posts?filter[discussion]=196428&page[offset]=0&page[limit]=20', f'postsindex_196428_off0_{TS}.json')
time.sleep(1)

# 2. Медиа-бекап ТГК 3197 (прецедент телескопа <1.5 ч)
MEDIA = [
    ('https://cdn4.telesco.pe/file/NEFox936a2roNtuDMOMjNN9SdtiUCYEYmkdyfQsurqMpY7DXDDCDogeel0bb7F1oQoyAOckVxPHCIr5RMZyKYdxw6NA5o60kE42nbUOwA87Wg_g7dCVZdfYw_1ozjyPApEqBicHrKLlx15TBlf9aQIyak-l_j5ZWms8u4ck-9n9_Z-X4No3Y-LFm9X1VoIBFzwitkui3Lbv8pazg5uv6K8eJjQSViOaNkZ95Wp6OG5zCoaZtEZwSGgFbfPTVz3NYtpNOK6N-DW84aLVk1gkuKRvo-rcAz040JmK2tHQ5N7qlFLRrfoXgvkmOImavKd_HAH_962VE4l6z8bj_V65y4Q.jpg', 'tg3197_media1.jpg'),
    ('https://cdn4.telesco.pe/file/HGC6-z7aOrEAVVkaKA1M1x6TICGXVKL02ymjD4WWGgzqE7qeohzjUoniEoQM9KwCEhLuyYU7KzRWCWvMofLriSEYF09_2T-KNgScVdKCtTvM63idoESzT-AMHcPKjdRaNaSjwYEdttayx_8lyhj1kdNQtt1TWVIldhOlT8e0fnla7qJ2LDQjXLLM1QUiOiFy16PT-2syihovDbwqGleiXPrRVISWJwyGBA1OwzOGqcVoiBRLzbr88GmExoH-8uO_jeCj7vLKzerwKjY9o63CbBtR55zYAlK31gWPRVgmYTLDorBrW4UL9zXUbSAdN2HLpjJn04XV7fDlEG1bL4kHZQ.jpg', 'tg3197_media2.jpg'),
]
for url, fname in MEDIA:
    path = os.path.join(OUT, f'forumcdn_tg3197_{fname}_{TS}')
    if os.path.exists(path):
        print(f'SKIP (exists) {fname}')
        done += 1
        continue
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA['User-Agent']})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        with open(path, 'wb') as f:
            f.write(body)
        sha = hashlib.sha256(body).hexdigest()
        print(f'OK {fname} ({len(body)}B) sha256={sha[:16]}')
        done += 1
    except Exception as e:
        print(f'FAIL {fname}: {type(e).__name__}: {e}')
        fail += 1
    time.sleep(1)

print(f'\nDONE: ok={done} fail={fail}')
