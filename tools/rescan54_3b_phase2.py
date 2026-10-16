#!/usr/bin/env python3
# rescan54_3b_phase2.py — Task 54-3 phase 2: хвосты из снапов TS 0327 — 196524 (Глеб #100+),
# 196424 ОТС (новый пост после удаления #93), 196411 union, 196435/196501/196514 tails, ТГК 3205?
import json, os, re

TS = '20261016_0327'
OUT = '/home/z/my-project/output/evidence_post'

def posts_of(fname):
    try:
        d = json.load(open(os.path.join(OUT, fname)))
    except Exception as e:
        print(f'PARSE FAIL {fname}: {e}'); return []
    data = d.get('data')
    items = data if isinstance(data, list) else [data] if data else []
    out = []
    for i in items:
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    return out

def head_text(p, n=170):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or ''
    if not t:
        t = a.get('contentHtml') or ''
    if not isinstance(t, str):
        t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:n]

def tail_posts(fname, start=None, n=12):
    pp = sorted(posts_of(fname), key=lambda p: p.get('attributes', {}).get('number') or 0)
    cnt = 0
    for p in pp:
        a = p.get('attributes', {})
        num = a.get('number') or 0
        if (start is None or num >= start) and cnt < n:
            print(f"  #{num} {a.get('createdAt','')[:19]} :: {head_text(p)}")
            cnt += 1

print('===== 196524 ГЛЕБ #100+ =====')
tail_posts(f'discussion_196524_near999999_{TS}.json', start=100)

print('\n===== 196424 ОТС #94+ (после удаления #93) =====')
tail_posts(f'discussion_196424_near999999_{TS}.json', start=93)

print('\n===== 196411 union =====')
union = set()
for off in ('off0', 'off20', 'off40'):
    for p in posts_of(f'postsindex_196411_{off}_{TS}.json'):
        union.add(p.get('attributes', {}).get('number'))
for p in posts_of(f'discussion_196411_near999999_{TS}.json'):
    union.add(p.get('attributes', {}).get('number'))
nums = sorted(n for n in union if n)
gaps = sorted(set(range(1, nums[-1] + 1)) - set(nums))
print(f'union 1..{nums[-1]}, гэпы: {gaps}')

print('\n===== 196435 tail #137+ =====')
tail_posts(f'discussion_196435_near999999_{TS}.json', start=137, n=4)
print('\n===== 196501 tail =====')
tail_posts(f'discussion_196501_near999999_{TS}.json', start=25, n=3)
print('\n===== 196514 tail =====')
tail_posts(f'discussion_196514_near999999_{TS}.json', start=14, n=3)

print('\n===== ТГК =====')
try:
    html = open(os.path.join(OUT, f'tg_stalzone_page0_{TS}.html'), encoding='utf-8', errors='ignore').read()
    msgs = []
    for m in re.finditer(r'data-post="stalzone/(\d+)"[\s\S]*?<time datetime="([^"]+)"[\s\S]*?(?:<div class="tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>)?[\s\S]*?(?=data-post="stalzone/|</section>)', html):
        mid, ts2, txt = m.group(1), m.group(2), m.group(3) or ''
        txt = re.sub(r'<br/?>', ' ', txt)
        txt = re.sub(r'<[^>]+>', '', txt)
        txt = re.sub(r'\s+', ' ', txt).strip()
        msgs.append((int(mid), ts2[:16], txt))
    for mid, ts2, txt in msgs[-4:]:
        print(f'  [{mid}] {ts2} :: {txt[:100]}')
except Exception as e:
    print(f'TG parse fail: {e}')
