# -*- coding: utf-8 -*-
# analyze54_134.py — (1) вырез-линия cc/LPN 1435-vs-1534 по кортежу (метод 54-133);
# (2) Пост Санити: реакции/лайки #14590/#14591, посты после #14591, наезды;
# (3) TG: подписи медиа 3223/7895; (4) 191614 mid near7185 контент.
import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'
PREV_TS, CUR_TS = '20261021_1435', '20261021_1534'

def attrs(ts, tid):
    fn = os.path.join(OUT, f'discussion_{tid}_near999999_{ts}.json')
    if not os.path.exists(fn): return None
    try:
        d = json.load(open(fn))
        return d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
    except Exception:
        return None

# --- 1) вырез-линия по кортежу (все near999999 снапы текущего TS) ---
print('===== ВЫРЕЗ-ЛИНИЯ (cc/LPN 1435 vs 1534; LPN_delta > cc_delta => CUT?) =====')
tids = sorted({int(m.group(1)) for f in glob.glob(os.path.join(OUT, f'discussion_*_near999999_{CUR_TS}.json'))
               for m in [re.match(r'discussion_(\d+)_near999999', os.path.basename(f))]})
cuts = 0
for tid in tids:
    a0, a1 = attrs(PREV_TS, tid), attrs(CUR_TS, tid)
    if not a1: print(f'[{tid}] нет снапа {CUR_TS}'); continue
    if not a0:
        print(f'[{tid}] NEW-тред или нет снапа 1435: cc={a1.get("commentCount")} LPN={a1.get("lastPostNumber")}')
        continue
    cc0, lp0 = a0.get('commentCount') or 0, a0.get('lastPostNumber') or 0
    cc1, lp1 = a1.get('commentCount') or 0, a1.get('lastPostNumber') or 0
    dcc, dlp = cc1 - cc0, lp1 - lp0
    flag = ''
    if dlp > dcc:
        flag = f' <<< CUT? вырезано ~{dlp - dcc}'; cuts += 1
    if dcc or dlp or flag:
        print(f'[{tid}] cc {cc0}->{cc1} ({dcc:+d}), LPN {lp0}->{lp1} ({dlp:+d}){flag}')
print(f'>>> вырез-линия: {cuts} тредов с подозрением (метод: только дельты за окно)')

# --- 2) Пост Санити: реакции/лайки ---
print('\n===== ПОСТ САНЕТИ (159759): #14590/#14591 реакции + хвост после #14591 =====')
try:
    d = json.load(open(os.path.join(OUT, f'discussion_159759_near999999_{CUR_TS}.json')))
    posts = [i for i in (d.get('data') if isinstance(d.get('data'), list) else []) if isinstance(i, dict) and i.get('type') == 'posts']
    posts += [i for i in (d.get('included') or []) if isinstance(i, dict) and i.get('type') == 'posts']
    users = {i['id']: (i.get('attributes', {}) or {}).get('username') for i in (d.get('included') or []) if i.get('type') == 'users'}
    for p in sorted(posts, key=lambda x: x.get('attributes', {}).get('number') or 0):
        a = p.get('attributes', {})
        n = a.get('number') or 0
        if n < 14588: continue
        uid = ((p.get('relationships', {}) or {}).get('user', {}) or {}).get('data', {})
        uid = uid.get('id') if isinstance(uid, dict) else None
        rc = a.get('reactionCounts') or {}
        print(f"  #{n} {a.get('createdAt','?')[:19]} {users.get(uid,'?')} likes={a.get('likesCount')} rx={rc} :: {re.sub(chr(60)+'[^'+chr(62)+']+'+chr(62),' ',(a.get('contentPlain') or '')[:90])}")
    after = [p for p in posts if (p.get('attributes', {}).get('number') or 0) > 14591]
    print(f'>>> постов после #14591: {len(after)}')
except Exception as e:
    print(f'159759 fail: {e}')

# --- 3) TG подписи медиа ---
print('\n===== TG подписи: 3223 (stalzone) / 7895 (spectrum) =====')
for ch, mid in (('stalzone', '3223'), ('spectrum_zone', '7895')):
    fn = os.path.join(OUT, f'tg_{ch}_page0_{CUR_TS}.html')
    if not os.path.exists(fn): print(f'{ch}: нет файла'); continue
    html = open(fn, encoding='utf-8', errors='ignore').read()
    i = html.find(f'data-post="{ch}/{mid}"')
    seg_h = html[i:i+4000] if i >= 0 else ''
    cap = re.search(r'tgme_widget_message_text[^>]*>([\s\S]*?)</div>', seg_h)
    ph = len(re.findall(r'tgme_widget_message_photo_wrap', seg_h))
    vid = len(re.findall(r'tgme_widget_message_video_wrap|tgme_widget_message_video_player', seg_h))
    txt = re.sub(r'<[^>]+>', ' ', cap.group(1)) if cap else ''
    txt = re.sub(r'\s+', ' ', txt).strip()
    print(f'{ch}/{mid}: photos={ph} video={vid} caption="{txt[:220]}"')

# --- 4) 191614 mid near7185 ---
print('\n===== 191614 середина near=7185 (fast-rule +16) =====')
fn = os.path.join(OUT, f'discussion_191614_near7185_{CUR_TS}.json')
if os.path.exists(fn):
    d = json.load(open(fn))
    posts = [i for i in (d.get('data') if isinstance(d.get('data'), list) else []) if isinstance(i, dict) and i.get('type') == 'posts']
    posts += [i for i in (d.get('included') or []) if isinstance(i, dict) and i.get('type') == 'posts']
    users = {i['id']: (i.get('attributes', {}) or {}).get('username') for i in (d.get('included') or []) if i.get('type') == 'users'}
    for p in sorted(posts, key=lambda x: x.get('attributes', {}).get('number') or 0)[-6:]:
        a = p.get('attributes', {})
        uid = ((p.get('relationships', {}) or {}).get('user', {}) or {}).get('data', {})
        uid = uid.get('id') if isinstance(uid, dict) else None
        print(f"  #{a.get('number')} {a.get('createdAt','?')[11:19]} {users.get(uid,'?')} :: {re.sub(chr(60)+'[^'+chr(62)+']+'+chr(62),' ',(a.get('contentPlain') or ''))[:110]}")
else:
    print('нет файла near7185')
