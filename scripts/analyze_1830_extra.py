#!/usr/bin/env python3
# analyze_1830_extra.py — union 196411 + canon #48 + TGK + front/news NEW из снапов 1830.
import json, os, re, hashlib

OUT = '/home/z/my-project/output/evidence_post'
TS = '20261018_1830'
CANON48 = 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e'

def items_of(d, typ):
    out = []
    data = d.get('data')
    items = data if isinstance(data, list) else [data] if data else []
    for i in items:
        if isinstance(i, dict) and i.get('type') == typ:
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == typ:
            out.append(i)
    return out

print('===== UNION 196411 (1830) =====')
union = set()
for off in ('off0', 'off20', 'off40'):
    fn = os.path.join(OUT, f'postsindex_196411_{off}_{TS}.json')
    try:
        d = json.load(open(fn))
        for p in items_of(d, 'posts'):
            n = p.get('attributes', {}).get('number')
            if n: union.add(n)
    except Exception as e:
        print(f'{off} fail: {e}')
try:
    d = json.load(open(os.path.join(OUT, f'discussion_196411_near999999_{TS}.json')))
    for p in items_of(d, 'posts'):
        n = p.get('attributes', {}).get('number')
        if n: union.add(n)
except Exception as e:
    print(f'near fail: {e}')
nums = sorted(union)
gaps = sorted(set(range(1, nums[-1] + 1)) - set(nums))
print(f'>>> union = 1..{nums[-1]}, всего живых {len(nums)}, гэпы: {gaps}')

print('===== CANON #48 (1830) =====')
for off in ('off0', 'off20', 'off40'):
    fn = os.path.join(OUT, f'postsindex_196411_{off}_{TS}.json')
    try:
        d = json.load(open(fn))
        for p in items_of(d, 'posts'):
            if p.get('attributes', {}).get('number') == 48:
                h = hashlib.sha256((p['attributes'].get('contentHtml') or '').encode()).hexdigest()
                rx = sum((p['attributes'].get('reactionCounts') or {}).values())
                print(f'#48 ({off}): sha256 {h[:16]}... {"CANON OK" if h == CANON48 else "!!! ИЗМЕНИЛСЯ"} rx={rx}')
    except Exception as e:
        print(f'#48 {off} fail: {e}')

print('===== TGK stalzone (1830) =====')
try:
    html = open(os.path.join(OUT, f'tg_stalzone_page0_{TS}.html'), encoding='utf-8', errors='ignore').read()
    msgs = []
    for m in re.finditer(r'data-post="stalzone/(\d+)"[\s\S]*?<time datetime="([^"]+)"[\s\S]*?(?:<div class="tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>)?[\s\S]*?(?=data-post="stalzone/|</section>)', html):
        mid, ts, txt = m.group(1), m.group(2), m.group(3) or ''
        txt = re.sub(r'<br/?>', ' ', txt)
        txt = re.sub(r'<[^>]+>', '', txt)
        txt = re.sub(r'\s+', ' ', txt).strip()
        msgs.append((int(mid), ts[:16], txt))
    for mid, ts, txt in msgs[-8:]:
        print(f'  [{mid}] {ts} :: {txt[:110]}')
except Exception as e:
    print(f'TG parse fail: {e}')

print('===== FRONT + NEWS NEW (1830) =====')
KNOWN = {196452, 196488, 196480, 196411, 196428, 196078, 196062, 196315, 196415, 196283,
         196424, 196461, 196490, 196511, 196469, 196474, 196475, 188595, 196326, 195079,
         195660, 195574, 195773, 196497, 196505, 196506, 196509, 196501, 196500, 196498,
         196514, 196513, 196435, 196434, 196510, 196516, 196519, 196520, 196499,
         196522, 196523, 196524, 196525, 196521, 196526, 196527, 196528, 196518,
         196529, 196530, 196531, 196496, 196260, 196100, 196258, 196532, 196536, 196533, 196537, 196539,
         196425, 196551, 196541, 196542, 196543, 196552, 196557, 196559, 196548, 196560, 196561, 196563, 196558, 196567, 196562, 196570, 196568, 196576, 196575, 196574, 196572, 196556, 196578, 196544, 196577, 196582, 196573, 196569, 196585, 196584, 196583, 196581, 196586, 196593, 196592, 196571, 196605, 196596, 196626, 196627, 196620,
         196621, 196630, 196637, 196638, 196639, 196640, 196641, 196642, 196643, 196644,
         196646, 193777, 196564, 196588, 196610, 196611, 196612, 196618, 187993, 196623,
         196624, 196625, 196628, 196629, 196631, 196633, 196634, 196635, 196150, 174335,
         185811, 196427, 196223, 195082, 196434, 196652, 196650, 196613, 196653, 196657,
         196658, 196661, 196656}
for fname, tag in ((f'frontindex_off0_{TS}.json', 'FRONT'), (f'tagnews_off0_{TS}.json', 'NEWS')):
    try:
        d = json.load(open(os.path.join(OUT, fname)))
    except Exception as e:
        print(f'{tag} fail: {e}'); continue
    seen = set()
    for i in items_of(d, 'discussions'):
        did = i.get('id')
        if did in seen: continue
        seen.add(did)
        a = i.get('attributes', {})
        try: didn = int(did)
        except Exception: didn = -1
        mark = ' [NEW]' if (didn not in KNOWN and didn > 196400) else ''
        if tag == 'FRONT' and (a.get('lastPostedAt', '') >= '2026-10-18T17:30' or mark):
            print(f"  {tag} [{did}] {a.get('lastPostedAt','?')[:16]} cc={a.get('commentCount')} :: {a.get('title','')[:80]}{mark}")
        elif tag == 'NEWS' and (a.get('lastPostedAt', '') >= '2026-10-16' or mark):
            print(f"  {tag} [{did}] {a.get('lastPostedAt','?')[:16]} cc={a.get('commentCount')} :: {a.get('title','')[:80]}{mark}")
