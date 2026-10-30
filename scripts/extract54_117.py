# extract54_117.py — собрать фактические LPN/cc из снапов 54-116 (TS 2030 + phase2 2040 + extra 2045)
import json, os, glob

OUT = '/home/z/my-project/output/evidence_post'
TIDS = [195081, 196718, 196721, 196727, 196730, 196732, 196734, 196735, 196739, 196742,
        196745, 196747, 196748, 196749, 196750, 196752, 196754, 196757, 196760, 196756,
        196763, 196762, 196755, 196758, 196764, 196765, 196761, 196766, 174560,
        196532, 196702, 196610, 196708, 187993, 196452, 196424, 196425, 196411, 196369]

def latest_snap(tid, near='999999'):
    pats = sorted(glob.glob(os.path.join(OUT, f'discussion_{tid}_near{near}_*.json')))
    return pats[-1] if pats else None

for tid in TIDS:
    near = '1' if tid in (174560, 196369) else '999999'
    p = latest_snap(tid, near)
    if not p:
        # попробуем другой near
        p = latest_snap(tid, '1') or latest_snap(tid, '999999')
        if not p:
            print(f'{tid}: NO SNAP'); continue
    try:
        d = json.load(open(p))
        aa = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
        print(f"{tid}: LPN={aa.get('lastPostNumber')} cc={aa.get('commentCount')} last={str(aa.get('lastPostedAt'))[:16]} src={os.path.basename(p)}")
    except Exception as e:
        print(f'{tid}: FAIL {e}')
