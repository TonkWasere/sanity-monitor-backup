# analyze54_140.py — вырез-линия 54-140: поснапная сверка cc/LPN двух TS-слоёв
# (2031 = 54-139 vs 2130 = 54-140) по всем ключам PREV_LPN + кортежа.
# Подозрение = cc_delta != lpn_delta (удаление/скрытие) или LPN упал.
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
PREV_TS, CUR_TS = '20261021_2031', '20261021_2130'

PREV_LPN = {191614: 7228, 196749: 44, 196755: 47, 196758: 25, 196770: 124, 196773: 95, 196777: 66, 196778: 41, 196794: 25,
            196801: 13, 196803: 20, 196804: 4, 196805: 31, 196808: 6, 196809: 31, 196810: 51, 196811: 5, 196812: 10, 196813: 19, 196815: 7, 196816: 16, 196817: 24,
            159759: 14599, 112917: 67705, 187993: 1251, 195081: 1076, 196718: 115, 196721: 18, 196727: 38, 196730: 32, 196732: 27, 196734: 55,
            196735: 38, 196739: 13, 196742: 13, 196745: 14, 196747: 4, 196748: 45, 196750: 13, 196752: 28, 196754: 11, 196756: 23,
            196757: 1, 196760: 33, 196761: 30, 196762: 4, 196763: 50, 196764: 11, 196765: 19, 196766: 1, 196767: 34, 196768: 8,
            196771: 16, 196772: 33, 196781: 4, 196782: 7, 196783: 13, 196784: 40, 196785: 26, 196786: 36, 196787: 3, 196788: 45,
            196791: 58, 196795: 11, 196797: 35, 196799: 67}

def attrs_of(tid, ts):
    hits = glob.glob(os.path.join(OUT, f'discussion_{tid}_near999999_{ts}.json')) + \
           glob.glob(os.path.join(OUT, f'discussion_{tid}_near1_{ts}.json'))
    if not hits:
        return None
    try:
        d = json.load(open(hits[0]))
        dd = d.get('data', {})
        return dd.get('attributes', {}) if isinstance(dd, dict) else {}
    except Exception:
        return None

susp, rows = [], []
for tid, prev_lpn in sorted(PREV_LPN.items()):
    pa, ca = attrs_of(tid, PREV_TS), attrs_of(tid, CUR_TS)
    if ca is None:
        rows.append(f'{tid}: нет текущего снапа (SKIP)')
        continue
    cc, lpn = ca.get('commentCount'), ca.get('lastPostNumber')
    if pa is not None:
        pcc, plpn = pa.get('commentCount'), pa.get('lastPostNumber')
        d_cc, d_lpn = (cc or 0) - (pcc or 0), (lpn or 0) - (plpn or 0)
        flag = ' <<< ПОДОЗРЕНИЕ (удаления?)' if (d_cc != d_lpn or d_lpn < 0) else ''
        rows.append(f'{tid}: cc {pcc}->{cc} (d{d_cc:+d}), LPN {plpn}->{lpn} (d{d_lpn:+d}){flag}')
        if d_cc != d_lpn or d_lpn < 0:
            susp.append(tid)
    else:
        # prev-снапа нет (NEW прошлого раунда) — сверяем с PREV_LPN-словарём
        d_lpn = (lpn or 0) - prev_lpn
        rows.append(f'{tid}: LPN {prev_lpn}->{lpn} (d{d_lpn:+d}, prev из словаря №181/№181-Б)')
        if d_lpn < 0:
            susp.append(tid)

print(f'=== ВЫРЕЗ-ЛИНИЯ 54-140: {PREV_TS} vs {CUR_TS} ({len(PREV_LPN)} ключей) ===')
for r in rows:
    print(r)
print(f'\n>>> ПОДОЗРЕНИЙ: {len(susp)} {susp if susp else "— линия ЧИСТА"}')
