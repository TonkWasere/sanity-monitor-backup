#!/usr/bin/env python3
# analyze_1830.py — восстановление дельт оборванного раунда 54-66 из снапов TS 20261018_1830.
# База сравнения = №109 (17:27-17:38 UTC): cc из шапки rescan54_66_fetch.py.
import json, os, re, sys

OUT = '/home/z/my-project/output/evidence_post'
TS = '20261018_1830'
# База №109 (17:27-17:38 UTC) — cc на момент записи
BASE109 = {
    196661: 9, 196656: 11, 196657: 17, 196620: 54, 196658: 13, 196653: 5,
    196652: 10, 196650: 16, 196640: None, 196641: 20, 196642: None,
    196643: 31, 196644: None, 196646: 37, 196626: 132, 196627: None, 196638: None,
    196621: None, 196548: 66, 196561: 36, 193777: 28, 185811: 224, 195080: None,
    195081: None, 196630: None, 196624: 52, 196623: None, 196631: None, 196633: None,
    196634: None, 196564: None, 196635: None, 196588: None, 196427: None, 196637: None,
    196639: None, 196625: None, 196628: None, 196629: None, 196610: None, 196150: None,
    174335: None, 196612: 38, 196618: None, 196611: None, 187993: None, 196572: None,
    196434: None, 196501: None, 196382: None, 179857: None, 195082: None, 196223: None,
    196452: 20, 196488: 45, 196480: 171, 196511: 31, 196524: 1147, 196475: 252,
    196522: None, 196523: None, 196411: 87, 196424: 160, 196461: None, 196435: None,
    196510: None, 196520: None, 196499: None, 196516: None, 196513: None, 196531: None,
    196496: None, 196260: None, 196428: None, 196078: None, 196062: None,
    196315: 87, 196415: 6, 196283: 82, 196425: 122, 196552: None, 196557: None,
    196537: 35, 196539: 30, 196551: None, 196542: None, 196543: None,
    196532: 292, 196536: 8, 196533: 2,
}

def posts_of(d):
    out = []
    data = d.get('data')
    items = data if isinstance(data, list) else [data] if data else []
    for i in items:
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    return out

def head_text(p, n=90):
    a = p.get('attributes', {})
    t = a.get('contentPlain') or a.get('content') or a.get('contentHtml') or ''
    if not isinstance(t, str):
        try: t = json.dumps(t, ensure_ascii=False)
        except Exception: t = str(type(t))
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()[:n]

for fn in sorted(os.listdir(OUT)):
    m = re.match(r'discussion_(\d+)_near999999_20261018_1830\.json$', fn)
    if not m:
        continue
    tid = int(m.group(1))
    try:
        d = json.load(open(os.path.join(OUT, fn)))
    except Exception as e:
        print(f'[{tid}] PARSE FAIL {e}')
        continue
    dd = d.get('data')
    aa = dd.get('attributes', {}) if isinstance(dd, dict) else {}
    cc = aa.get('commentCount')
    lpn = aa.get('lastPostNumber')
    base = BASE109.get(tid)
    dl = (cc - base) if (cc is not None and base is not None) else None
    pp = posts_of(d)
    tail = sorted(pp, key=lambda p: p.get('attributes', {}).get('number') or 0)[-2:]
    last_time = (tail[-1].get('attributes', {}).get('createdAt') or '')[:16] if tail else ''
    dl_s = f'{dl:+d}' if dl is not None else ' ? '
    cc_s = str(cc) if cc is not None else '?'
    print(f'[{tid}] cc={cc_s} (base {base} {dl_s}) lpn={lpn} last={last_time}')
    for p in tail:
        a = p.get('attributes', {})
        print(f"   #{a.get('number')} {(a.get('createdAt') or '')[:16]} :: {head_text(p)}")
