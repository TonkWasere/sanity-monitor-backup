#!/usr/bin/env python3
# analyze54_116.py — сводка дельт раунда 54-116 по снапам TS 2030 (+ phase-2 2040).
import json, os, re, hashlib

TS = '20261020_2030'
OUT = f'/home/z/my-project/output/evidence_post'

PREV_LPN = {195081: 1075, 196718: 112, 196721: 18, 196727: 38, 196730: 32, 196732: 27,
            196734: 53, 196735: 37, 196739: 13, 196742: 13, 196745: 14, 196747: 4,
            196748: 31, 196749: 18, 196750: 13, 196752: 19, 196754: 11, 196757: 1,
            196760: 29, 196756: 22, 196763: 20, 196762: 2, 196755: 9, 196758: 21,
            196764: 6, 196765: 2, 196761: 6}
KNOWN = {196452, 196488, 196480, 196411, 196428, 196078, 196062, 196315, 196415, 196283,
         196424, 196425, 196435, 196461, 196511, 195081, 196718, 196721, 196727, 196730,
         196731, 196732, 196733, 196734, 196735, 196736, 196737, 196739, 196742, 196745,
         196747, 196748, 196749, 196750, 196752, 196754, 196757, 196760, 196756, 196729,
         196624, 196689, 196704, 196706, 196708, 196510, 196688, 196699, 196701, 196702,
         196703, 196655, 196705, 196714, 196715, 196716, 196667, 196665, 196548, 195080,
         195083, 196646, 196621, 196626, 196501, 196643, 196475, 196532, 196496, 196260,
         196524, 196522, 196523, 196513, 196516, 196720, 196722, 196724, 196725, 187993,
         196763, 196762, 196755, 196758, 196764, 196765, 196761}

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

print('===== 1. FRONT-INDEX: NEW-кандидаты (lastPostedAt >= 19:27) =====')
fi = load(f'frontindex_off0_{TS}.json')
newc = []
for i in (fi.get('data') or []) + (fi.get('included') or []):
    if isinstance(i, dict) and i.get('type') == 'discussions':
        a = i.get('attributes', {})
        tid = i.get('id')
        if a.get('lastPostedAt', '') >= '2026-10-20T19:27':
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
                                             196736, 196737, 196461, 196435, 196548, 196610]))
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
for tid, label, prevcc in [(187993, 'Братство Пульса', 1190)]:
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

print('\n===== 4. 196411 UNION-КАРТА + КАНОН (урок 54-113: + near999999) =====')
seen = {}
for off in (0, 20, 40):
    d = load(f'postsindex_196411_off{off}_{TS}.json')
    if not d:
        print(f'  off{off}: NO SNAP'); continue
    for i in (d.get('data') or []) + (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            n = i.get('attributes', {}).get('number')
            if n: seen[n] = i.get('id')
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
a = attrs(196411)
print(f'  196411 cc={a.get("commentCount")} LPN={a.get("lastPostNumber")}' if a else '  196411: NO SNAP')

print('\n===== 5. НОВОСТИ (tagnews) =====')
tn = load(f'tagnews_off0_{TS}.json')
for i in (tn.get('data') or [])[:8]:
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

print('\n===== 7. OP NEW (phase-2, TS 2040) =====')
d = load('discussion_196766_near1_20261020_2040.json')
if d:
    a = d.get('data', {}).get('attributes', {})
    print(f"  [196766] «{a.get('title','')}» createdAt={a.get('createdAt','')[:16]} cc={a.get('commentCount')} LPN={a.get('lastPostNumber')}")
else:
    print('  196766: NO PHASE2')
