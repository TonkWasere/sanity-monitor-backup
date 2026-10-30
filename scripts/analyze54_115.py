#!/usr/bin/env python3
# analyze54_115.py — сводка дельт раунда 54-115 по снапам TS 1932 (+ phase-2 1947).
import json, os, re, hashlib

TS = '20261020_1932'
OUT = f'/home/z/my-project/output/evidence_post'

PREV_LPN = {195081: 1074, 196718: 112, 196721: 18, 196727: 38, 196730: 32, 196732: 27,
            196734: 53, 196735: 37, 196739: 13, 196742: 13, 196745: 14, 196747: 4,
            196748: 29, 196749: 17, 196750: 13, 196752: 19, 196754: 11, 196757: 1,
            196760: 29, 196756: 22, 196763: 19, 196762: 2, 196755: 9, 196758: 21}
KNOWN = {196452, 196488, 196480, 196411, 196428, 196078, 196062, 196315, 196415, 196283,
         196424, 196425, 196435, 196461, 196511, 195081, 196718, 196721, 196727, 196730,
         196731, 196732, 196733, 196734, 196735, 196736, 196737, 196739, 196742, 196745,
         196747, 196748, 196749, 196750, 196752, 196754, 196757, 196760, 196756, 196729,
         196624, 196689, 196704, 196706, 196708, 196510, 196688, 196699, 196701, 196702,
         196703, 196655, 196705, 196714, 196715, 196716, 196667, 196665, 196548, 195080,
         195083, 196646, 196621, 196626, 196501, 196643, 196475, 196532, 196496, 196260,
         196524, 196522, 196523, 196513, 196516, 196720, 196722, 196724, 196725, 187993,
         196763, 196762, 196755, 196758}

def load(fn):
    try:
        return json.load(open(os.path.join(OUT, fn)))
    except Exception as e:
        return None

def attrs(tid, near='999999'):
    d = load(f'discussion_{tid}_near{near}_{TS}.json')
    if not d: return None
    a = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
    return a

print('===== 1. FRONT-INDEX: NEW-кандидаты (lastPostedAt >= 18:27) =====')
fi = load(f'frontindex_off0_{TS}.json')
newc = []
for i in (fi.get('data') or []) + (fi.get('included') or []):
    if isinstance(i, dict) and i.get('type') == 'discussions':
        a = i.get('attributes', {})
        tid = i.get('id')
        if a.get('lastPostedAt', '') >= '2026-10-20T18:27':
            tag = 'NEW?' if int(tid) not in KNOWN else 'known'
            print(f"  {tid} cc={a.get('commentCount')} LPN={a.get('lastPostNumber')} last={a.get('lastPostedAt','')[:16]} [{tag}] «{a.get('title','')[:60]}»")
            if int(tid) not in KNOWN:
                newc.append(int(tid))
print('NEW candidates:', newc)

print('\n===== 2. ДЕЛЬТЫ ХВОСТОВ (PREV -> now) =====')
tails = sorted(set(list(PREV_LPN.keys()) + [196745, 196747, 196510, 196708, 196731, 196689,
                                             196704, 196706, 196702, 196703, 196655, 196705,
                                             196714, 196715, 196716, 196667, 196665, 195080,
                                             195083, 196646, 196621, 196626, 196501, 196643,
                                             196475, 196532, 196496, 196260, 196524, 196624,
                                             196688, 196699, 196701, 196522, 196523, 196513,
                                             196516, 196720, 196722, 196724, 196725, 196733,
                                             196736, 196737, 196461, 196435, 196548]))
for tid in tails:
    a = attrs(tid)
    if a is None:
        print(f'  [{tid}] NO SNAP'); continue
    cc, lpn = a.get('commentCount'), a.get('lastPostNumber')
    prev = PREV_LPN.get(tid)
    delta = (lpn - prev) if (lpn is not None and prev is not None) else '?'
    locked = ' LOCKED' if a.get('isLocked') else ''
    print(f'  [{tid}] cc={cc} LPN={lpn} (prev {prev}, delta {delta}){locked} last={a.get("lastPostedAt","")[:16]}')

print('\n===== 2b. БОЛЬШИЕ (cc-сравнение) =====')
for tid, label, prevcc in [(112917, 'вайб', 66418), (187993, 'Братство Пульса', 1190),
                           (196424, 'ОТС', None), (196425, 'ОТС-фидбек', None),
                           (196452, 'Талоны', None), (196411, '196411', None)]:
    a = attrs(tid)
    if a is None:
        print(f'  [{tid}] {label}: NO SNAP'); continue
    cc = a.get('commentCount')
    d = f' (delta {cc - prevcc})' if prevcc else ''
    print(f'  [{tid}] {label}: cc={cc}{d} LPN={a.get("lastPostNumber")} last={a.get("lastPostedAt","")[:16]}')

print('\n===== 3. КЛЮЧЕВЫЕ ЛИНИИ =====')
for tid, label in [(196424, 'ОТС 196424'), (196425, 'ОТС-фидбек 196425'), (196452, 'Талоны'),
                   (196488, 'Кейс-шансы 196488'), (196480, 'Кейс 196480'), (196511, 'Хотфикс'),
                   (196428, '196428'), (196283, 'контроль 196283'), (196078, 'магпулы 196078'),
                   (196062, '196062'), (196315, 'контроль 196315'), (196415, 'контроль 196415')]:
    a = attrs(tid)
    if a is None:
        print(f'  [{tid}] {label}: NO SNAP'); continue
    print(f'  [{tid}] {label}: cc={a.get("commentCount")} LPN={a.get("lastPostNumber")} last={a.get("lastPostedAt","")[:16]} locked={a.get("isLocked")}')

print('\n===== 4. 196411 UNION-КАРТА + КАНОН #48 (урок 54-113: + near999999) =====')
seen = {}
for off in (0, 20, 40):
    d = load(f'postsindex_196411_off{off}_{TS}.json')
    if not d:
        print(f'  off{off}: NO SNAP'); continue
    for i in (d.get('data') or []) + (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            n = i.get('attributes', {}).get('number')
            if n: seen[n] = i.get('id')
# урок 54-113: near999999-посты тоже в union
d999 = load(f'discussion_196411_near999999_{TS}.json')
if d999:
    posts = d999.get('included') or []
    if not posts and isinstance(d999.get('data'), list): posts = d999['data']
    for i in posts:
        if isinstance(i, dict) and i.get('type') == 'posts':
            n = i.get('attributes', {}).get('number')
            if n: seen[n] = i.get('id')
nums = sorted(seen)
gaps = []
for a_, b_ in zip(nums, nums[1:]):
    if b_ - a_ > 1: gaps.append((a_, b_))
print(f'  union posts: {len(nums)} (1..{max(nums) if nums else 0}), gaps={[g for g in gaps if g[1]-g[0]>1]}')
a = attrs(196411, 'near1')
print(f'  196411 cc={a.get("commentCount")} LPN={a.get("lastPostNumber")}')

d = load(f'postsindex_196411_off0_{TS}.json')
canon_ok = False
for i in (d.get('data') or []) + (d.get('included') or []):
    if isinstance(i, dict) and i.get('type') == 'posts' and i.get('attributes', {}).get('number') == 48:
        body = i.get('attributes', {}).get('contentHtml') or i.get('attributes', {}).get('content') or ''
        h = hashlib.sha256(body.encode('utf-8')).hexdigest()
        canon_ok = (h == 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e')
        print(f'  #48 sha256={h[:16]}... CANON {"OK" if canon_ok else "MISMATCH!"}')

print('\n===== 5. НОВОСТИ (tagnews) =====')
tn = load(f'tagnews_off0_{TS}.json')
for i in (tn.get('data') or [])[:10]:
    if isinstance(i, dict) and i.get('type') == 'discussions':
        a = i.get('attributes', {})
        print(f"  {i.get('id')} «{a.get('title','')[:55]}» last={a.get('lastPostedAt','')[:16]} cc={a.get('commentCount')}")

print('\n===== 6. ТГК stalzone =====')
try:
    html = open(os.path.join(OUT, f'tg_stalzone_page0_{TS}.html'), encoding='utf-8', errors='ignore').read()
    ids = [int(x) for x in re.findall(r'data-post="stalzone/(\d+)"', html)]
    print('  посты на странице:', ids[:5], '...', ids[-3:] if len(ids) > 5 else '')
except Exception as e:
    print('  NO TGK SNAP:', e)

print('\n===== 7. OP NEW (phase-2, TS 1947) =====')
for tid in (196764, 196765, 196761):
    d = load(f'discussion_{tid}_near1_20261020_1947.json')
    if not d:
        print(f'  [{tid}] NO PHASE2'); continue
    a = d.get('data', {}).get('attributes', {})
    print(f"  [{tid}] «{a.get('title','')}» createdAt={a.get('createdAt','')[:16]} cc={a.get('commentCount')} LPN={a.get('lastPostNumber')}")
