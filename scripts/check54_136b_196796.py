#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 54-136b: межраундовая верификация сноса 196796 «По-русски говори».
# Автор (логин-юзер) сообщил: тред 404 и для залогиненного -> СНЕСЁН, не скрыт от гостей.
# Гость перепроверяет: статус /api/discussions/196796 + HTML-страница, снапы с TS.
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

TS = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
OUT = '/home/z/my-project/output/evidence_post'
BASE = 'https://forum.exbo.net'


def fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Accept': 'application/json, text/html;q=0.9,*/*;q=0.8',
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')[:2000]
    except Exception as e:  # noqa: BLE001
        return -1, str(e)


results = {}

# 1) API статус треда 196796 (ожидаем 404)
st, body = fetch(f'{BASE}/api/discussions/196796')
results['api_196796_status'] = st
results['api_196796_body_head'] = body[:500]
with open(f'{OUT}/196796_api_status_{TS}.json', 'w') as f:
    json.dump({'url': f'{BASE}/api/discussions/196796', 'status': st,
               'body_head': body[:500], 'ts_utc': datetime.now(timezone.utc).isoformat()},
              f, ensure_ascii=False, indent=2)
print(f"API 196796 -> HTTP {st}")
time.sleep(1)

# 2) HTML-страница треда (ожидаем 404 или ошибку)
st2, body2 = fetch(f'{BASE}/d/196796')
results['html_196796_status'] = st2
with open(f'{OUT}/196796_html_status_{TS}.txt', 'w') as f:
    f.write(f"url={BASE}/d/196796\nstatus={st2}\nts={TS}\n")
print(f"HTML /d/196796 -> HTTP {st2}")
time.sleep(1)

# 3) Контроль живого треда 159759 (гость видит 200 = сеть/API живы, 404 не сбой сети)
st3, body3 = fetch(f'{BASE}/api/discussions/159759?page[near]=14591')
results['control_159759_status'] = st3
if st3 == 200:
    d = json.loads(body3)
    posts = d.get('data', {}).get('posts', [])
    lpn = max((p.get('number', 0) for p in posts), default=0)
    results['control_159759_lpn_in_window'] = lpn
    print(f"Контроль 159759 -> HTTP 200, LPN в окне = {lpn}")
else:
    print(f"Контроль 159759 -> HTTP {st3}")

with open(f'{OUT}/check54_136b_summary_{TS}.json', 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print('---')
print(json.dumps(results, ensure_ascii=False, indent=2))
