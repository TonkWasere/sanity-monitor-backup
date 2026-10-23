#!/usr/bin/env python3
# cuts_delta_180.py — что поймано ПОСЛЕ аудита 54-175-audit (граница 14:45 UTC, TS1430)
# Строгий критерий аудита: пост был в снапе A, отсутствует в снапе B, диапазон B накрывает.
# Пары: 1530→1630→1730→1830→1930. Новые вырезы = не в теле аудита (608 с текстом).
import json, os, re
from collections import defaultdict

OUT = '/home/z/my-project/output/evidence_post'
TS_LIST = ['20261023_1530', '20261023_1630', '20261023_1730', '20261023_1830', '20261023_1930']
TS_HR = {'20261023_1530': '15:30', '20261023_1630': '16:30', '20261023_1730': '17:30',
         '20261023_1830': '18:30', '20261023_1930': '19:30'}
AUDIT = '/home/z/my-project/output/08_monitoring/cut_texts_audit_20261023.txt'

audit_body = defaultdict(set)
for line in open(AUDIT, encoding='utf-8'):
    m = re.match(r'^--- \[(\d+)\] #(\d+) ', line)
    if m:
        audit_body[int(m.group(1))].add(int(m.group(2)))

# --- снапы: tid -> ts -> {num: post} (один файл на tid/ts: приоритет near999999) ---
# + lpn/cc по data.attributes
snaps = defaultdict(dict)
lpn_cc = {}
tids = set()
for fn in sorted(os.listdir(OUT)):
    m = re.match(r'discussion_(\d+)_(near\w+)_(20261023_1[5-9]30)\.json', fn)
    if not m:
        continue
    tid, near, ts = int(m.group(1)), m.group(2), m.group(3)
    tids.add(tid)
    if ts in snaps[tid] and near != 'near999999':
        continue  # уже есть более приоритетный
    if ts in snaps[tid] and near == 'near1':
        continue
    try:
        d = json.load(open(os.path.join(OUT, fn)))
    except Exception:
        continue
    posts = {}
    for p in d.get('included', []):
        if p.get('type') == 'posts':
            n = p.get('attributes', {}).get('number')
            if isinstance(n, int):
                posts[n] = p
    if posts:
        snaps[tid][ts] = posts
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        lpn_cc[tid] = (aa.get('lastPostNumber'), aa.get('commentCount'))

def head_text(p, n=170):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('contentHtml') or ''
    if not isinstance(t, str):
        t = str(t)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()[:n]

print('===== НОВЫЕ ВЫРЕЗЫ ПОСЛЕ АУДИТА (пары 15:30→19:30) =====')
new_by_thread = defaultdict(list)
for tid in sorted(tids):
    series = [ts for ts in TS_LIST if ts in snaps[tid] and snaps[tid][ts]]
    for i in range(len(series) - 1):
        A, B = series[i], series[i + 1]
        pa, pb = snaps[tid][A], snaps[tid][B]
        lo, hi = min(pb), max(pb)
        for num in sorted(pa):
            if lo <= num <= hi and num not in pb and num not in audit_body[tid]:
                p = pa[num]
                new_by_thread[tid].append((num, TS_HR[B], head_text(p)))

total_new = 0
for tid in sorted(new_by_thread):
    lst = sorted(set(new_by_thread[tid]))
    total_new += len(lst)
    print(f'\n[{tid}] новых вырезов: {len(lst)}')
    for num, caught_at, text in lst:
        print(f'  #{num} (исчез к {caught_at}) :: {text}')

print('\n===== ДЫРЫ (номера с вырезом, никогда не снившиеся с текстом) =====')
for tid in sorted(tids):
    if tid not in lpn_cc:
        continue
    lpn, cc = lpn_cc[tid]
    if not isinstance(lpn, int) or not isinstance(cc, int) or lpn <= cc:
        continue
    last = [ts for ts in TS_LIST if ts in snaps[tid]]
    if not last:
        continue
    caught_now = set(snaps[tid][last[-1]].keys()) | audit_body[tid]
    for n, b, t in new_by_thread[tid]:
        caught_now.add(n)
    missing = sorted(set(range(1, lpn + 1)) - caught_now)
    if missing:
        print(f'  [{tid}] гэп={lpn - cc} (LPN {lpn}/cc {cc}): не снились {missing[:30]}{"..." if len(missing) > 30 else ""} ({len(missing)} шт.)')
print(f'\nИТОГО новых вырезов после аудита: {total_new}')
