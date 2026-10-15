#!/usr/bin/env python3
# rescan54_18_analyze.py — разбор дельт раунда 54-18 vs база 1834 (Task 53)
import json, os, hashlib, re

OUT = '/home/z/my-project/output/evidence_post'
CANON48 = 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e'
NEW_TS = '20261015_1852'
OLD_TS = '20261015_1834'

def disc_ids(fname):
    try:
        d = json.load(open(os.path.join(OUT, fname)))
    except Exception as e:
        print(f'FAIL {fname}: {e}'); return []
    res = []
    data = d.get('data')
    for i in (data if isinstance(data, list) else [data] if data else []):
        if isinstance(i, dict) and i.get('type') == 'discussions':
            a = i.get('attributes', {})
            res.append((int(i.get('id', 0)), a.get('lastPostedAt', '')[:16], a.get('commentCount'), a.get('title', '')[:70]))
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'discussions':
            a = i.get('attributes', {})
            res.append((int(i.get('id', 0)), a.get('lastPostedAt', '')[:16], a.get('commentCount'), a.get('title', '')[:70]))
    return res

# 1. News-витрина (полная, top-18)
print('===== NEWS TAG INDEX (top-18, TS 1852) =====')
news = disc_ids(f'tagnews_off0_{NEW_TS}.json')
seen = set(); uniq = []
for t in news:
    if t[0] in seen: continue
    seen.add(t[0]); uniq.append(t)
for t in uniq[:18]:
    print(f'  [{t[0]}] {t[1]} cc={t[2]} :: {t[3]}')

# 2. Классификация "новых" тредов фронта: были ли в 1834?
print('\n===== КЛАССИФИКАЦИЯ NEW-тредов (в 1834? в news?) =====')
old_front = {t[0] for t in disc_ids(f'frontindex_off0_{OLD_TS}.json')}
old_news = {t[0] for t in disc_ids(f'tagnews_off0_{OLD_TS}.json')}
new_front = {t[0] for t in disc_ids(f'frontindex_off0_{NEW_TS}.json')}
new_news = {t[0] for t in disc_ids(f'tagnews_off0_{NEW_TS}.json')}
for tid in (196461, 196509, 196505, 196497, 196506):
    was_front = 'фронт1834=ДА' if tid in old_front else 'фронт1834=НЕТ'
    was_news = 'news1834=ДА' if tid in old_news else 'news1834=НЕТ'
    now_news = 'news1852=ДА' if tid in new_news else 'news1852=НЕТ'
    in_now = 'фронт1852=ДА' if tid in new_front else 'фронт1852=НЕТ'
    print(f'  [{tid}]: {was_front}, {was_news}; {in_now}, {now_news}')

# 3. Дельта news-витрины 1834 -> 1852
print('\n===== NEWS-ВИТРИНА ДЕЛЬТА (1834 -> 1852) =====')
gone = sorted(old_news - new_news)
came = sorted(new_news - old_news)
print(f'  ушло из news-витрины: {gone}')
print(f'  появилось в news-витрине: {came}')

# 4. #48 sha256 по union (postsindex 1852)
print('\n===== #48 CANON по union (TS 1852) =====')
found = False
for off in ('off0', 'off20', 'off40'):
    try:
        d = json.load(open(os.path.join(OUT, f'postsindex_196411_{off}_{NEW_TS}.json')))
    except Exception:
        continue
    items = d.get('data') if isinstance(d.get('data'), list) else ([d.get('data')] if d.get('data') else [])
    for i in (items + (d.get('included') or [])):
        if isinstance(i, dict) and i.get('type') == 'posts' and i.get('attributes', {}).get('number') == 48:
            h = hashlib.sha256((i['attributes'].get('contentHtml') or '').encode()).hexdigest()
            rx = sum((i['attributes'].get('reactionCounts') or {}).values())
            print(f'  #48 ({off}): sha256 {h} {"CANON OK" if h == CANON48 else "!!! ИЗМЕНИЛСЯ"} rx={rx} likes={i["attributes"].get("likesCount")}')
            found = True
            break
    if found: break
if not found:
    print('  #48 НЕ НАЙДЕН в postsindex union — тревога')

# 5. 196424: полный список постов #81-87 (свежая вспышка)
print('\n===== 196424 ОТС: хвост #81-87 =====')
try:
    d = json.load(open(os.path.join(OUT, f'discussion_196424_near999999_{NEW_TS}.json')))
    items = d.get('data') if isinstance(d.get('data'), list) else ([d.get('data')] if d.get('data') else [])
    posts = [i for i in (items + (d.get('included') or [])) if isinstance(i, dict) and i.get('type') == 'posts']
    for p in sorted(posts, key=lambda x: x.get('attributes', {}).get('number') or 0):
        n = p['attributes'].get('number')
        if n and n >= 81:
            t = re.sub(r'<[^>]+>', ' ', p['attributes'].get('contentHtml') or p['attributes'].get('contentPlain') or '')
            t = re.sub(r'\s+', ' ', t).strip()[:150]
            print(f"  #{n} {p['attributes'].get('createdAt','')[:19]} :: {t}")
except Exception as e:
    print(f'  FAIL 196424: {e}')
