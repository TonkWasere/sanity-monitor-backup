#!/usr/bin/env python3
# analyze54_208.py — локальный пересчёт дельт TS2320 vs prev_lpn_208 (без сети)
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
TS = '20261024_2320'

prev = {int(k): v for k, v in json.load(open('/tmp/prev_lpn_208.json')).items()}
cur = {}
for fn in glob.glob(os.path.join(OUT, f'discussion_*_near999999_{TS}.json')):
    m = re.match(r'discussion_(\d+)_near999999_' + TS + r'\.json', os.path.basename(fn))
    if not m:
        continue
    try:
        d = json.load(open(fn))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        lpn, cc = aa.get('lastPostNumber'), aa.get('commentCount')
        hid = aa.get('isHidden')
        if lpn is None:
            continue
        cur[int(m.group(1))] = {'lpn': lpn, 'cc': cc, 'hidden': hid}
    except Exception as e:
        print(f'parse fail {fn}: {e}')

print(f'=== TS2320 снято: {len(cur)} тредов (prev база {len(prev)}) ===')

up, down, gap_new, vanish, hidden = [], [], [], [], []
for tid, v in sorted(cur.items()):
    p = prev.get(tid)
    if not p:
        continue
    dl, dc = v['lpn'] - p['lpn'], v['cc'] - p['cc']
    gap = v['lpn'] - v['cc']
    pgap = p['lpn'] - p['cc']
    if dl or dc:
        up.append((tid, p['lpn'], p['cc'], v['lpn'], v['cc'], dl, dc, gap))
    if dl < 0 or dc < 0:
        down.append((tid, p, v))
    if gap > pgap:
        gap_new.append((tid, pgap, gap))
    if v.get('hidden'):
        hidden.append((tid, v['hidden']))
for tid in prev:
    if tid not in cur:
        vanish.append(tid)

print(f'--- ДЕЛЬТЫ ВВЕРХ ({len(up)}): tid prev->cur (+lpn/+cc) гэп')
for tid, pl, pc, cl, cc2, dl, dc, gap in sorted(up, key=lambda x: -x[5]):
    print(f'  {tid}: {pl}/{pc} -> {cl}/{cc2} (+{dl}/+{dc}) гэп={gap}')
print(f'--- ВНИЗ/СНОСЫ ({len(down)}): {down}')
print(f'--- ГЭП ВЫРОС (вырезы) ({len(gap_new)}): {gap_new}')
print(f'--- HIDDEN ({len(hidden)}): {hidden}')
print(f'--- VANISH vs prev ({len(vanish)}): {vanish}')

# NEW: near1-файлы этого часа (OP свежих из newlist) вне prev
n1 = set()
for fn in glob.glob(os.path.join(OUT, f'discussion_*_near1_{TS}.json')):
    m = re.match(r'discussion_(\d+)_near1_' + TS + r'\.json', os.path.basename(fn))
    if m:
        n1.add(int(m.group(1)))
print(f'--- near1 OP-файлы {TS}: {sorted(n1)} (вне prev: {sorted(n1 - set(prev))})')

# 404: KNOWN из rescan54_208 без файла TS2320
src = open('/home/z/my-project/tools/rescan54_208_fetch.py', encoding='utf-8').read()
m = re.search(r'KNOWN\s*=\s*\{([^}]*)\}', src, re.S)
known = {int(x) for x in re.findall(r'\d{5,7}', m.group(1))} if m else set()
miss404 = sorted(t for t in known if t not in cur)
print(f'--- KNOWN={len(known)}, 404-FAIL ({len(miss404)}): {miss404}')

# все файлы часа
allf = glob.glob(os.path.join(OUT, f'*_{TS}.*'))
print(f'--- всего файлов {TS}: {len(allf)}')
