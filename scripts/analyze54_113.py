#!/usr/bin/env python3
# analyze54_113.py — сводка дельт раунда 54-113 по снапам TS 1731.
import json, os, re, hashlib

TS = '20261020_1731'
OUT = f'/home/z/my-project/output/evidence_post'

PREV_LPN = {195081: 1073, 196718: 108, 196721: 18, 196727: 38, 196730: 32, 196732: 27,
            196734: 53, 196735: 31, 196739: 13, 196742: 12, 196745: 14, 196747: 4,
            196748: 27, 196749: 13, 196750: 13, 196752: 15, 196754: 11, 196757: 1,
            196760: 14, 196756: 18}
KNOWN = {196452, 196488, 196480, 196411, 196428, 196078, 196062, 196315, 196415, 196283,
         196424, 196425, 196435, 196461, 196511, 195081, 196718, 196721, 196727, 196730,
         196731, 196732, 196733, 196734, 196735, 196736, 196737, 196739, 196742, 196745,
         196747, 196748, 196749, 196750, 196752, 196754, 196757, 196760, 196756, 196729,
         196624, 196689, 196704, 196706, 196708, 196510, 196688, 196699, 196701, 196702,
         196703, 196655, 196705, 196714, 196715, 196716, 196667, 196665, 196548, 195080,
         195083, 196646, 196621, 196626, 196501, 196643, 196475, 196532, 196496, 196260,
         196524, 196522, 196523, 196513, 196516, 196720, 196722, 196724, 196725, 187993}

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

print('===== 1. FRONT-INDEX: NEW-кандидаты (lastPostedAt >= 16:27) =====')
fi = load(f'frontindex_off0_{TS}.json')
newc = []
for i in (fi.get('data') or []) + (fi.get('included') or []):
    if isinstance(i, dict) and i.get('type') == 'discussions':
        a = i.get('attributes', {})
        tid = i.get('id')
        if a.get('lastPostedAt', '') >= '2026-10-20T16:27':
            tag = 'NEW?' if int(tid) not in KNOWN else 'known'
            print(f"  {tid} cc={a.get('commentCount')} LPN={a.get('lastPostNumber')} last={a.get('lastPostedAt')} [{tag}] «{a.get('title','')[:60]}»")
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
                                             196736, 196737, 196461, 196435]))
for tid in tails:
    a = attrs(tid)
    if a is None:
        print(f'  [{tid}] NO SNAP'); continue
    cc, lpn = a.get('commentCount'), a.get('lastPostNumber')
    prev = PREV_LPN.get(tid)
    delta = (lpn - prev) if (lpn is not None and prev is not None) else '?'
    locked = ' LOCKED' if a.get('isLocked') else ''
    print(f'  [{tid}] cc={cc} LPN={lpn} (prev {prev}, delta {delta}){locked} last={a.get("lastPostedAt","")[:16]}')

print('\n===== 3. КЛЮЧЕВЫЕ ЛИНИИ =====')
for tid, label in [(196424, 'ОТС 196424'), (196425, 'ОТС-фидбек 196425'), (196452, 'Талоны'),
                   (196488, 'Кейс-шансы 196488'), (196480, 'Кейс 196480'), (196511, 'Хотфикс'),
                   (196428, '196428'), (196283, 'контроль 196283'), (196078, 'магпулы 196078'),
                   (196062, '196062'), (196315, 'контроль 196315'), (196415, 'контроль 196415')]:
    a = attrs(tid)
    if a is None:
        print(f'  [{tid}] {label}: NO SNAP'); continue
    print(f'  [{tid}] {label}: cc={a.get("commentCount")} LPN={a.get("lastPostNumber")} last={a.get("lastPostedAt","")[:16]} locked={a.get("isLocked")}')

print('\n===== 4. 196411 UNION-КАРТА + КАНОН #48 =====')
seen = {}
for off in (0, 20, 40):
    d = load(f'postsindex_196411_off{off}_{TS}.json')
    if not d:
        print(f'  off{off}: NO SNAP'); continue
    for i in (d.get('data') or []) + (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            n = i.get('attributes', {}).get('number')
            if n: seen[n] = i.get('id')
nums = sorted(seen)
gaps = []
for a_, b_ in zip(nums, nums[1:]):
    if b_ - a_ > 1: gaps.append((a_, b_))
print(f'  union posts: {len(nums)} (1..{max(nums) if nums else 0}), gaps={[g for g in gaps if g[1]-g[0]>1]}')
d = load(f'discussion_196411_near1_{TS}.json')
a = attrs(196411, 'near1')
print(f'  196411 cc={a.get("commentCount")} LPN={a.get("lastPostNumber")}')

# канон #48 по off0
d = load(f'postsindex_196411_off0_{TS}.json')
canon_ok = False; rx = None
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
html = open(os.path.join(OUT, f'tg_stalzone_page0_{TS}.html'), encoding='utf-8', errors='ignore').read()
ids = [int(x) for x in re.findall(r'data-post="stalzone/(\d+)"', html)]
print('  посты на странице:', ids[:5], '...', ids[-3:] if len(ids) > 5 else '')
