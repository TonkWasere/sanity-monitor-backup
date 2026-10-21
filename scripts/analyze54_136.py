# analyze54_136.py — вырез-линия + дельты: сверка cc/LPN снапов 1634 (54-135) vs 1733 (54-136).

import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
PREV_TS, CUR_TS = '20261021_1634', '20261021_1733'
PREV_LPN = {191614: 7218, 196749: 40, 196755: 47, 196758: 25, 196770: 121, 196773: 88, 196777: 62, 196778: 41, 196794: 25, 196796: 53,
            196801: 11, 196803: 19, 196804: 4, 196805: 23, 196808: 6, 196809: 18, 196811: 5, 159759: 14591, 112917: 67696, 187993: 1232,
            195081: 1076, 196718: 115, 196721: 18, 196727: 38, 196730: 32, 196732: 27, 196734: 55, 196735: 38, 196739: 13, 196742: 13,
            196745: 14, 196747: 4, 196748: 45, 196750: 13, 196752: 28, 196754: 11, 196756: 23, 196757: 1, 196760: 33, 196761: 30,
            196762: 4, 196763: 49, 196764: 11, 196765: 17, 196766: 1, 196767: 34, 196768: 8, 196771: 16, 196772: 30, 196781: 4,
            196782: 7, 196783: 13, 196784: 39, 196785: 26, 196786: 33, 196787: 3, 196788: 45, 196791: 48, 196795: 9, 196797: 35, 196799: 27}

def attrs(ts, tid):
    fn = os.path.join(OUT, f'discussion_{tid}_near999999_{ts}.json')
    if not os.path.exists(fn):
        return None
    try:
        d = json.load(open(fn))
        return d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
    except Exception:
        return None

print('=== ВЫРЕЗ-ЛИНИЯ: cc/LPN 1634 vs 1733 ===')
suspects = []
rows = []
for tid, plpn in sorted(PREV_LPN.items()):
    pa, ca = attrs(PREV_TS, tid), attrs(CUR_TS, tid)
    if tid == 196796:
        print(f'[196796] 1634 cc=? LPN=53 -> 1733: 404 (файла нет, подтверждено re-fetch) — ТРЕД СНЕСЁН/СКРЫТ')
        suspects.append(tid)
        continue
    if ca is None:
        print(f'[{tid}] 1733 снапа нет (SKIP)')
        continue
    cc_n, lpn_n = ca.get('commentCount') or 0, ca.get('lastPostNumber') or 0
    if pa:
        cc_p = pa.get('commentCount') or 0
        lpn_p = pa.get('lastPostNumber') or plpn
    else:
        cc_p, lpn_p = None, plpn
    d_cc = (cc_n - cc_p) if cc_p is not None else None
    d_lpn = lpn_n - lpn_p
    flag = ''
    if d_cc is not None and (d_cc < 0 or (d_lpn > d_cc)):
        flag = ' <<< ВЫРЕЗ?'
        suspects.append(tid)
    rows.append((tid, cc_p, cc_n, lpn_p, lpn_n, d_cc, d_lpn, flag))
    print(f'[{tid}] cc {cc_p}->{cc_n} ({d_cc}), LPN {lpn_p}->{lpn_n} (+{d_lpn}){flag}')

print(f'\n>>> подозрений: {suspects if suspects else 0}')

print('\n=== 159759: посты после #14591 ===')
fn = os.path.join(OUT, f'discussion_159759_near999999_{CUR_TS}.json')
d = json.load(open(fn))
posts = [i for i in (d.get('included') or []) if i.get('type') == 'posts']
after = [p for p in posts if ((p.get('attributes', {}) or {}).get('number') or 0) > 14591]
print(f'постов после #14591 в окне: {len(after)}')

print('\n=== ТГК stalzone ===')
try:
    html = open(os.path.join(OUT, f'tg_stalzone_page0_{CUR_TS}.html'), encoding='utf-8', errors='ignore').read()
    msgs = []
    for m in re.finditer(r'data-post="stalzone/(\d+)"[\s\S]*?<time datetime="([^"]+)"[\s\S]*?(?:<div class="tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>)?[\s\S]*?(?=data-post="stalzone/|</section>)', html):
        txt = re.sub(r'<br/?>', ' ', m.group(3) or '')
        txt = re.sub(r'<[^>]+>', '', txt)
        txt = re.sub(r'\s+', ' ', txt).strip()
        msgs.append((int(m.group(1)), m.group(2)[:16], txt))
    for mid, ts, txt in msgs[-5:]:
        print(f'  [{mid}] {ts} :: {txt[:100]}')
except Exception as e:
    print(f'TG fail: {e}')

print('\n=== ТГК Спектрума ===')
try:
    html2 = open(os.path.join(OUT, f'tg_spectrum_page0_{CUR_TS}.html'), encoding='utf-8', errors='ignore').read()
    msgs2 = []
    for m in re.finditer(r'data-post="spectrum_zone/(\d+)"[\s\S]*?<time datetime="([^"]+)"[\s\S]*?(?:<div class="tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>)?[\s\S]*?(?=data-post="spectrum_zone/|</section>)', html2):
        txt2 = re.sub(r'<br/?>', ' ', m.group(3) or '')
        txt2 = re.sub(r'<[^>]+>', '', txt2)
        txt2 = re.sub(r'\s+', ' ', txt2).strip()
        msgs2.append((int(m.group(1)), m.group(2)[:16], txt2))
    for mid2, ts2, txt2 in msgs2[-5:]:
        print(f'  [{mid2}] {ts2} :: {txt2[:100]}')
except Exception as e:
    print(f'TG-SPEC fail: {e}')
