#!/usr/bin/env python3
# rescan54_18b_phase2.py — Task 54-18: OP новых тредов 196561/196563/196558 (near1+near999999)
# + хвосты 196559/196548/196560/196501/196434 + ТГК 3207 текст.
import json, os, re, time, urllib.request, hashlib

BASE = 'https://forum.exbo.net'
OUT = '/home/z/my-project/output/evidence_post'
TS = '20261016_1829'
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
            json.loads(data.decode('utf-8'))  # валидация
        print('OK', fname, f'({len(data)}B)'); time.sleep(1); return True
    except Exception as e:
        print('FAIL', fname, e); return False

# --- OP новых тредов окна 18:26 ---
for tid in (196561, 196563, 196558):
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json')
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json')
# --- хвосты вспыхнувших ---
for tid in (196559, 196548, 196560, 196501, 196434):
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json')

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

def dump_thread(tid):
    fnear = os.path.join(OUT, f'discussion_{tid}_near999999_{TS}.json')
    fop = os.path.join(OUT, f'discussion_{tid}_near1_{TS}.json')
    src = fnear if os.path.exists(fnear) else fop
    if not os.path.exists(src):
        print(f'[{tid}] NO DATA'); return
    try:
        d = json.load(open(src, encoding='utf-8'))
        load_users(os.path.basename(src))
        dd = d.get('data', {})
        aa = dd.get('attributes', {}) if isinstance(dd, dict) else {}
        title = aa.get('title', '?'); cc = aa.get('commentCount'); lpn = aa.get('lastPostNumber')
        created = (aa.get('createdAt') or '')[:16]
        print(f"\n===== {tid} «{title}» cc={cc} LPN={lpn} created={created} =====")
        # OP
        if os.path.exists(fop):
            dop = json.load(open(fop, encoding='utf-8'))
            inc = dop.get('included', [])
            for i in inc:
                if i.get('type') == 'users':
                    users[i['id']] = i.get('attributes', {}).get('username') or f"u{i['id']}"
            opp = [p for p in dop.get('included', []) if p.get('type') == 'posts' and p.get('attributes', {}).get('number') == 1]
            if opp:
                opa = opp[0].get('attributes', {})
                txt = opa.get('contentPlain') or ''
                if not txt:
                    h = opa.get('contentHtml') or ''
                    txt = re.sub(r'<[^>]+>', ' ', h)
                    txt = re.sub(r'\s+', ' ', txt).strip()
                print(f"  OP[{uname(opp[0].get('relationships', {}).get('user', {}).get('data', {}).get('id'))}] {txt[:420]}")
        pp = []
        dd2 = d.get('data', {})
        posts_rel = (dd2.get('relationships', {}).get('posts', {}) or {}).get('data', [])
        included_posts = [i for i in d.get('included', []) if i.get('type') == 'posts']
        by_id = {i['id']: i for i in included_posts}
        for rel in posts_rel:
            p = by_id.get(rel.get('id'))
            if p: pp.append(p)
        for p in pp[-10:]:
            a = p.get('attributes', {})
            num = a.get('number'); ts = (a.get('createdAt') or '')[:16]
            uid = p.get('relationships', {}).get('user', {}).get('data', {}).get('id')
            txt = a.get('contentPlain') or ''
            if not txt:
                h = a.get('contentHtml') or ''
                txt = re.sub(r'<[^>]+>', ' ', h)
                txt = re.sub(r'\s+', ' ', txt).strip()
            print(f"  #{num} {ts} :: {uname(uid)} {txt[:200]}")
    except Exception as e:
        print(f'[{tid}] parse fail {e}')

for tid in (196561, 196563, 196558, 196559, 196548, 196560, 196501, 196434):
    dump_thread(tid)

# --- ТГК 3207 текст ---
print('\n===== ТГК 3207 =====')
try:
    html = open(os.path.join(OUT, 'tg_stalzone_page0_20261016_1828.html'), encoding='utf-8', errors='ignore').read()
    m = re.search(r'data-post="stalzone/3207"[\s\S]*?(?=data-post="stalzone/|$)', html)
    if m:
        blk = m.group(0)
        t = re.search(r'<time datetime="([^"]+)"', blk)
        tm = t.group(1) if t else '?'
        tx = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>', blk)
        txt = tx.group(1) if tx else '(без текста)'
        txt = re.sub(r'<br/?>', ' | ', txt)
        txt = re.sub(r'<[^>]+>', '', txt)
        txt = re.sub(r'\s+', ' ', txt).strip()
        print(f'[3207] {tm} :: {txt[:600]}')
        views = re.search(r'(\d[\dKM]*)\s*views', blk)
        print('views:', views.group(1) if views else '?')
    else:
        print('3207 не найден в HTML')
except Exception as e:
    print('TG fail', e)
