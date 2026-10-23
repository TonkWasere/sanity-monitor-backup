#!/usr/bin/env python3
# cut_posts_audit2.py — аудит вырезов v2: строгий критерий.
# Вырез = пост N был в TS_A, в TS_B ОТСУТСТВУЕТ, но диапазон номеров TS_B
# НАКРЫВАЕТ N (min(TS_B) <= N <= max(TS_B)) — значит его удалили, а не окно ушло.
# + достаём сохранённый текст из последнего снапа, где пост был.
import json, os, re, glob
from collections import defaultdict

OUT = '/home/z/my-project/output/evidence_post'
files = glob.glob(os.path.join(OUT, 'discussion_*_near999999_*.json')) + \
        glob.glob(os.path.join(OUT, 'discussion_*_near1_*.json')) + \
        glob.glob(os.path.join(OUT, 'discussion_*_near381_*.json')) + \
        glob.glob(os.path.join(OUT, 'discussion_*_near430_*.json'))
threads = defaultdict(set)
by_tt = defaultdict(dict)
for f in files:
    m = re.match(r'discussion_(\d+)_near(\d+)_(\d{8}_\d{4})\.json', os.path.basename(f))
    if m:
        tid, near, ts = int(m.group(1)), int(m.group(2)), m.group(3)
        key = (tid, near)
        threads[key].add(ts)
        by_tt[key][ts] = f

def posts_map(fname):
    try:
        d = json.load(open(fname))
    except Exception:
        return {}
    users = {u['id']: u['attributes'].get('username') for u in d.get('included', []) if u.get('type') == 'users'}
    pm = {}
    def walk(lst):
        for p in lst:
            if not isinstance(p, dict) or p.get('type') != 'posts':
                continue
            a = p.get('attributes', {})
            n = a.get('number')
            if n is None:
                continue
            uid = p.get('relationships', {}).get('user', {}).get('data', {}).get('id')
            txt = (a.get('contentPlain') or '')
            if not txt:
                txt = re.sub(r'<[^>]+>', ' ', a.get('contentHtml') or '')
            pm[n] = (a.get('createdAt', ''), users.get(uid, '?'), re.sub(r'\s+', ' ', txt).strip())
    dta = d.get('data')
    walk(dta if isinstance(dta, list) else [dta] if dta else [])
    walk(d.get('included', []))
    return pm

cuts = defaultdict(dict)  # tid -> num -> (ts_seen, meta, nearkey)
for key, tss in sorted(threads.items()):
    tss_sorted = sorted(tss)
    prev_pm, prev_ts = None, None
    for ts in tss_sorted:
        pm = posts_map(by_tt[key][ts])
        if prev_pm is not None and pm:
            lo, hi = min(pm), max(pm)
            for n, meta in prev_pm.items():
                if lo <= n <= hi and n not in pm and n not in cuts[key[0]]:
                    cuts[key[0]][n] = (prev_ts, meta, key[1])
        prev_pm, prev_ts = pm, ts

tot = sum(len(v) for v in cuts.values())
with_txt = sum(1 for v in cuts.values() for x in v.values() if x[1][2])
print(f'=== СТРОГИЙ АУДИТ: вырезов поймано {tot}, из них С СОХРАНЁННЫМ ТЕКСТОМ: {with_txt} ===')
print()
print('по тредам:')
for tid, nums in sorted(cuts.items()):
    t = sum(1 for x in nums.values() if x[1][2])
    print(f'  [{tid}]: вырезов {len(nums)}, с текстом {t}, номера: {sorted(nums)[:25]}{"..." if len(nums)>25 else ""}')
print()
print('=== СОХРАНЁННЫЕ ТЕКСТЫ ВЫРЕЗОВ (хронологически) ===')
rows = []
for tid, nums in cuts.items():
    for n, (ts_seen, (ca, user, txt), near) in nums.items():
        if txt:
            rows.append((ts_seen, tid, n, user, ca, txt, near))
rows.sort()
for ts_seen, tid, n, user, ca, txt, near in rows:
    print(f'--- [{tid}] #{n} {user} | {ca[:19]} | последний снап с текстом TS{ts_seen} (near{near})')
    print(f'    {txt[:400]}')
