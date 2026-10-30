#!/usr/bin/env python3
# analyze_0120.py — офлайн-разбор раунда 54-210 (stdout потерян пайпом):
# дельты prev_lpn_210(00:2x) -> prev_lpn_211(01:2x), ВЫРЕЗы, отсутствие (404),
# канон #48, young-потоки, NEW по фронту/новостям.
import json, glob, hashlib, re

MON = '/home/z/my-project'
prev = {int(k): v for k, v in json.load(open('/tmp/prev_lpn_210.json')).items()}
cur = {int(k): v for k, v in json.load(open('/tmp/prev_lpn_211.json')).items()}

print(f'база prev_lpn_210: {len(prev)} кл; current prev_lpn_211: {len(cur)} кл')

missing = sorted(set(prev) - set(cur))
if missing:
    print(f'ОТСУТСТВУЮТ в 01:2x (404/FAIL): {missing}')
else:
    print('ОТСУТСТВУЮЩИХ НЕТ (0 404 среди известных!)')

print('\n===== ДЕЛЬТЫ (lpn/cc 00:2x -> 01:2x) =====')
young = {196979, 196982, 196983, 196984}
n = 0
for tid in sorted(cur):
    o, c = prev.get(tid), cur[tid]
    if not o:
        print(f'  НОВЫЙ-КЛЮЧ {tid}: {c["lpn"]}/{c["cc"]}')
        continue
    dl, dc = c['lpn'] - o['lpn'], c['cc'] - o['cc']
    gap_o, gap_c = o['lpn'] - o['cc'], c['lpn'] - c['cc']
    if dl or dc or gap_c != gap_o:
        n += 1
        tag = ' [YOUNG]' if tid in young else ''
        extra = f' ВЫРЕЗ+{gap_c - gap_o} (гэп {gap_o}->{gap_c})' if gap_c > gap_o else ''
        extra += f' гэп-смягчение {gap_o}->{gap_c}' if gap_c < gap_o else ''
        print(f'  {tid}{tag}: {o["lpn"]}/{o["cc"]} -> {c["lpn"]}/{c["cc"]} (+{dl}/+{dc}){extra}')
print(f'итого тредов с дельтами: {n}')

# Канон #48
try:
    d = json.load(open(f'{MON}/output/evidence_post/postsindex_196411_off40_20261025_0120.json'))
    posts = []
    if isinstance(d.get('data'), list):
        posts += d['data']
    posts += d.get('included') or []
    p48 = [p for p in posts if isinstance(p, dict) and p.get('attributes', {}).get('number') == 48]
    for p in p48:
        a = p['attributes']
        for field in ('contentHtml', 'content', 'contentPlainText'):
            if field in a and a[field]:
                h = hashlib.sha256(a[field].encode()).hexdigest()
                if h == 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e':
                    print(f'\nКАНОН #48: MATCH ({field}, 84-й час OK)')
                    break
        else:
            print(f'\nКАНОН #48: sha256 НЕ совпал ни по одному полю (поля: {[k for k in a if "content" in k]})')
except Exception as e:
    print(f'канон-проверка error: {e}')

# NEW по фронту: createdAt <= 01:20 окна 00:20->01:20, вне prev-ключей
try:
    d = json.load(open(f'{MON}/output/evidence_post/frontindex_off0_20261025_0120.json'))
    discs = []
    if isinstance(d.get('data'), list):
        discs += d['data']
    discs += d.get('included') or []
    new = []
    for i in discs:
        if isinstance(i, dict) and i.get('type') == 'discussions':
            a = i.get('attributes') or {}
            ct = a.get('createdAt') or ''
            if ct >= '2026-10-25T00:20' and int(i.get('id')) not in prev and int(i.get('id')) not in cur:
                new.append((i.get('id'), a.get('title', '')[:40], ct, a.get('lastPostNumber'), a.get('commentCount')))
    print(f'\nNEW ФРОНТ (createdAt>=00:20, вне извест): {len(new)}')
    for x in new:
        print(f'  NEW {x[0]} «{x[1]}» {x[2]} lpn/cc {x[3]}/{x[4]}')
except Exception as e:
    print(f'front NEW error: {e}')

# 196411 заморозка + ключевые замеры
for tid in (196411, 196424, 196425, 196488, 196480, 196452, 196511, 196461, 196435, 196428, 196283, 196078, 196062, 196315, 196415, 191614, 112917):
    c = cur.get(tid)
    o = prev.get(tid)
    if c and o:
        print(f'  {tid}: {o["lpn"]}/{o["cc"]} -> {c["lpn"]}/{c["cc"]}' + (' [замерло]' if c == o else ' [ДВИЖЕНИЕ]'))
    elif c:
        print(f'  {tid}: {c["lpn"]}/{c["cc"]} (нет базы)')
    else:
        print(f'  {tid}: НЕТ СНАПА 0120')
