#!/usr/bin/env python3
# rescan54_29b_phase2.py — Task 54-29: утренняя волна.
# NEW: 196581 «Мастерская "Ножка"» (cc=5, 05:22) — OP+хвост.
# Оживший вне main-набора: 196355 «Снова о пластинах» (cc=161, 05:27 — старый тред).
import json, os, re, time, urllib.request

BASE = 'https://forum.exbo.net'
OUT = '/home/z/my-project/output/evidence_post'
TS = "20261017_0533"
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')

def get(url, fname):
    dst = os.path.join(OUT, fname)
    if os.path.exists(dst):
        print('SKIP', fname); return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        open(dst, 'wb').write(data)
        if fname.endswith('.json'):
            json.loads(data.decode('utf-8'))
        print('OK', fname, f'({len(data)}B)'); time.sleep(1); return True
    except Exception as e:
        print('FAIL', fname, e); return False

users = {}
def uname(uid):
    return users.get(uid, f'u{uid}')

def load_users(fname):
    try:
        d = json.load(open(os.path.join(OUT, fname), encoding='utf-8'))
        for i in d.get('included', []):
            if i.get('type') == 'users':
                users[i['id']] = i.get('attributes', {}).get('username') or f"u{i['id']}"
    except Exception as e:
        print('users fail', fname, e)

def dump_thread(tid, tail_n=10):
    fnear = os.path.join(OUT, f'discussion_{tid}_near999999_{TS}.json')
    if not os.path.exists(fnear):
        print(f'[{tid}] NO DATA'); return
    try:
        d = json.load(open(fnear, encoding='utf-8'))
        load_users(os.path.basename(fnear))
        dd = d.get('data', {})
        aa = dd.get('attributes', {}) if isinstance(dd, dict) else {}
        title = aa.get('title', '?'); cc = aa.get('commentCount'); lpn = aa.get('lastPostNumber')
        created = (aa.get('createdAt') or '')[:16]
        print(f"\n===== {tid} «{title}» cc={cc} LPN={lpn} created={created} =====")
        included_posts = [i for i in d.get('included', []) if i.get('type') == 'posts']
        by_id = {i['id']: i for i in included_posts}
        pp = [by_id[r['id']] for r in (dd.get('relationships', {}).get('posts', {}) or {}).get('data', []) if by_id.get(r['id'])]
        nums = sorted((p.get('attributes', {}).get('number') or 0) for p in pp)
        if nums:
            gaps = sorted(set(range(1, nums[-1] + 1)) - set(nums))
            print(f'  гэпы (видимая карта): {gaps}')
        for p in pp[-tail_n:]:
            a = p.get('attributes', {})
            num = a.get('number'); ts = (a.get('createdAt') or '')[:16]
            uid = p.get('relationships', {}).get('user', {}).get('data', {}).get('id')
            txt = a.get('contentPlain') or ''
            if not txt:
                h = a.get('contentHtml') or ''
                txt = re.sub(r'<[^>]+>', ' ', h)
                txt = re.sub(r'\s+', ' ', txt).strip()
            print(f"  #{num} {ts} :: {uname(uid)} {txt[:180]}")
    except Exception as e:
        print(f'[{tid}] parse fail {e}')

for tid in (196581, 196355):
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json')

for tid in (196581, 196355):
    dump_thread(tid)

print(f'\nTS={TS}')
