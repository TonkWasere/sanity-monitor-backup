# analyze54_130_ranks.py — ранги постеров в середине разогнавшихся тредов (54-130)
import json
OUT = '/home/z/my-project/output/evidence_post'
TS = '20261021_1133'
for tid, near in ((196791, 29), (196773, 22), (196788, 33)):
    try:
        d = json.load(open(f'{OUT}/discussion_{tid}_near{near}_{TS}.json'))
    except Exception as e:
        print(f'== {tid} near{near}: fail {e}'); continue
    groups = {i['id']: (i.get('attributes', {}) or {}).get('nameSingular') for i in (d.get('included') or []) if i.get('type') == 'groups'}
    users = {i['id']: i for i in (d.get('included') or []) if i.get('type') == 'users'}
    posts = [(p.get('attributes', {}).get('number'), p.get('relationships', {}).get('user', {}).get('data', {}).get('id'))
             for p in (d.get('included') or []) if p.get('type') == 'posts']
    print(f'== {tid} near{near} (постеры середины: группы/сообщения) ==')
    for num, uid in sorted(posts, key=lambda x: (x[0] or 0)):
        u = users.get(uid) or {}
        a = u.get('attributes', {})
        gs = [groups.get(x.get('id'), x.get('id')) for x in u.get('relationships', {}).get('groups', {}).get('data', [])]
        print(f'  #{num} {a.get("username")} {gs} cc={a.get("commentCount")}')
