#!/usr/bin/env python3
# cut_posts_audit.py — аудит вырезов в evidence: что реально сохранили.
# (1) isHidden=true посты в снапах + есть ли у них контент
# (2) посты, присутствовавшие в раннем TS-снапе и ИСЧЕЗШИЕ в позднем (снос между раундами)
#     + вытащить их текст из самого раннего снапа, где они были.
import json, os, re, glob
from collections import defaultdict

OUT = '/home/z/my-project/output/evidence_post'
files = glob.glob(os.path.join(OUT, 'discussion_*_near999999_*.json'))
threads = defaultdict(set)          # tid -> set(TS)
by_tt = defaultdict(dict)           # (tid,ts) -> fname
for f in files:
    m = re.match(r'discussion_(\d+)_near999999_(\d{8}_\d{4})\.json', os.path.basename(f))
    if m:
        tid, ts = int(m.group(1)), m.group(2)
        threads[tid].add(ts)
        by_tt[(tid, ts)] = f

def posts_map(fname):
    """num -> (createdAt, username, text) для всех постов в снапе."""
    try:
        d = json.load(open(fname))
    except Exception:
        return {}, {}
    users = {u['id']: u['attributes'].get('username') for u in d.get('included', []) if u.get('type') == 'users'}
    pm, hid = {}, {}
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
                h = a.get('contentHtml') or ''
                txt = re.sub(r'<[^>]+>', ' ', h)
            txt = re.sub(r'\s+', ' ', txt).strip()
            pm[n] = (a.get('createdAt', ''), users.get(uid, '?'), txt)
            if a.get('isHidden'):
                hid[n] = bool(txt)
    dta = d.get('data')
    walk(dta if isinstance(dta, list) else [dta] if dta else [])
    walk(d.get('included', []))
    return pm, hid

print('=== 1) isHidden=true прямо в снапах (API отдал объект, но пометил скрытым) ===')
hidden_total, hidden_with_content = 0, 0
hidden_by_thread = defaultdict(int)
for (tid, ts), f in sorted(by_tt.items()):
    _, hid = posts_map(f)
    for n, has_txt in hid.items():
        hidden_total += 1
        hidden_by_thread[tid] += 1
        if has_txt:
            hidden_with_content += 1
for tid, c in sorted(hidden_by_thread.items()):
    print(f'  [{tid}]: {c} скрытых объектов в снапах')
print(f'  ИТОГО скрытых объектов: {hidden_total}, из них С КОНТЕНТОМ: {hidden_with_content}')

print()
print('=== 2) СНОСЫ МЕЖДУ СНАПАМИ: был в раннем TS -> исчез в позднем ===')
vanished = defaultdict(dict)  # tid -> num -> (last_ts_seen, meta)
for tid, tss in sorted(threads.items()):
    tss_sorted = sorted(tss)
    prev_pm = None
    prev_ts = None
    for ts in tss_sorted:
        pm, _ = posts_map(by_tt[(tid, ts)])
        if prev_pm is not None:
            for n, meta in prev_pm.items():
                if n not in pm and n not in vanished[tid]:
                    vanished[tid][n] = (prev_ts, meta)
        prev_pm, prev_ts = pm, ts

tot_v, tot_content = 0, 0
rows = []
for tid, nums in sorted(vanished.items()):
    for n, (ts_seen, (ca, user, txt)) in sorted(nums.items()):
        tot_v += 1
        has = bool(txt)
        if has:
            tot_content += 1
        rows.append((tid, ts_seen, n, user, ca, has, txt))

print(f'  ИТОГО исчезнувших постов (снос между раундами): {tot_v}, из них С СОХРАНЁННЫМ ТЕКСТОМ: {tot_content}')
print()
print('=== 3) ТОП-примеры сохранённых текстов снесённых постов ===')
saved = [r for r in rows if r[5]]
saved.sort(key=lambda r: r[1])
shown = 0
for tid, ts_seen, n, user, ca, has, txt in saved:
    if shown >= 15:
        break
    print(f'  [{tid}] #{n} {user} {ca[:16]} (посл. раз в TS{ts_seen}): {txt[:220]}')
    shown += 1
if not saved:
    print('  (нет ни одного)')

print()
print('=== 4) Снесённые БЕЗ текста (поймали только номер) ===')
nosave = [r for r in rows if not r[5]]
from collections import Counter
cnt = Counter((r[0], r[1]) for r in nosave)
for (tid, ts), c in sorted(cnt.items())[:20]:
    print(f'  [{tid}] TS{ts}: {c} постов исчезло без текста')
