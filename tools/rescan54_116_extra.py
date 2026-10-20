#!/usr/bin/env python3
# rescan54_116_extra.py — добор: 174560 near1 (0 упоминаний в ledger, бамп на фронт).
import json, os, urllib.request, time, re

TS = '20261020_2045'
OUT = '/home/z/my-project/output/evidence_post'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
req = urllib.request.Request('https://forum.exbo.net/api/discussions/174560?sort=-lastPostedAt&page[near]=1', headers={'User-Agent': UA})
dst = f'{OUT}/discussion_174560_near1_{TS}.json'
body = urllib.request.urlopen(req, timeout=30).read()
json.loads(body.decode('utf-8'))
open(dst, 'wb').write(body)
print(f'OK {dst} ({len(body)}B)')
d = json.load(open(dst))
a = d.get('data', {}).get('attributes', {})
print(f"[174560] «{a.get('title','')}» createdAt={str(a.get('createdAt'))[:16]} cc={a.get('commentCount')} LPN={a.get('lastPostNumber')} locked={a.get('isLocked')}")
posts = sorted([i for i in (d.get('included') or []) if isinstance(i, dict) and i.get('type') == 'posts'], key=lambda p: p.get('attributes', {}).get('number') or 0)
for p in posts[:2]:
    pa = p.get('attributes', {})
    txt = re.sub('<[^>]+>', ' ', pa.get('contentHtml') or pa.get('content') or '')
    print('  #' + str(pa.get('number')), str(pa.get('createdAt'))[:16], '::', ' '.join(txt.split())[:160])
print('TS=' + TS)
