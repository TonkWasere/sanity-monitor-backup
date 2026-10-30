#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# analyze54_139.py — (1) вырез-линия: поснапная сверка cc/LPN 1934-vs-2031 по всем 65 ключам №180;
# (2) 159759: КТО написал #14592-#14596 (5 постов после 6 часов тишины; авторы по relationships.user —
# урок 54-137); (3) 196810: авторы постов после #41 (мод-реакция на наезд #35? офиц. ответ?).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
PREV_TS, CUR_TS = '20261021_1934', '20261021_2031'
PREV_LPN = {191614: 7228, 196749: 42, 196755: 47, 196758: 25, 196770: 124, 196773: 94, 196777: 66, 196778: 41,
            196794: 25, 196801: 13, 196803: 20, 196804: 4, 196805: 31, 196808: 6, 196809: 31, 196810: 41,
            196811: 5, 196813: 16, 196815: 7, 196816: 16, 196817: 21, 159759: 14591, 112917: 67705, 187993: 1251,
            195081: 1076, 196718: 115, 196721: 18, 196727: 38, 196730: 32, 196732: 27, 196734: 55,
            196735: 38, 196739: 13, 196742: 13, 196745: 14, 196747: 4, 196748: 45, 196750: 13, 196752: 28,
            196754: 11, 196756: 23, 196757: 1, 196760: 33, 196761: 30, 196762: 4, 196763: 50, 196764: 11,
            196765: 19, 196766: 1, 196767: 34, 196768: 8, 196771: 16, 196772: 33, 196781: 4, 196782: 7,
            196783: 13, 196784: 40, 196785: 26, 196786: 33, 196787: 3, 196788: 45, 196791: 58, 196795: 10,
            196797: 35, 196799: 67}


def attrs(tid, ts):
    fn = os.path.join(OUT, f'discussion_{tid}_near999999_{ts}.json')
    d = json.load(open(fn))
    return d.get('data', {}).get('attributes', {}) or {}


print('===== ВЫРЕЗ-ЛИНИЯ: cc/LPN 1934-vs-2031 (вырез = cc_delta < lpn_delta) =====')
susp = []
for tid, prev_lpn in sorted(PREV_LPN.items()):
    try:
        pa, ca = attrs(tid, PREV_TS), attrs(tid, CUR_TS)
        pcc, pcl = pa.get('commentCount'), pa.get('lastPostNumber')
        ccc, ccl = ca.get('commentCount'), ca.get('lastPostNumber')
        dcc, dlpn = (ccc - pcc), (ccl - pcl)
        mark = ''
        if dcc < dlpn:
            susp.append(tid)
            mark = ' <<< ВЫРЕЗ?'
        if dcc or dlpn:
            print(f'  [{tid}] cc {pcc}->{ccc} ({dcc:+}) | LPN {pcl}->{ccl} ({dlpn:+}){mark}')
    except FileNotFoundError:
        print(f'  [{tid}] снап {PREV_TS} отсутствует (пропуск)')
    except Exception as e:  # noqa: BLE001
        print(f'  [{tid}] fail: {e}')
print(f'>>> подозрений: {len(susp)} {susp if susp else ""}')


def users_groups(dd):
    users = {i['id']: (i.get('attributes', {}) or {}).get('username')
             for i in (dd.get('included') or []) if i.get('type') == 'users'}
    groups = {i['id']: (i.get('attributes', {}) or {}).get('nameSingular')
              for i in (dd.get('included') or []) if i.get('type') == 'groups'}
    ug = {}
    for i in (dd.get('included') or []):
        if i.get('type') == 'users':
            gids = [x.get('id') for x in (i.get('relationships', {}) or {}).get('groups', {}).get('data', [])]
            ug[i['id']] = [groups.get(g, g) for g in gids]
    return users, ug


def posts_after(dd, num_min):
    users, ug = users_groups(dd)
    seen = {}
    for i in (dd.get('data') if isinstance(dd.get('data'), list) else []) + (dd.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            a = i.get('attributes', {}) or {}
            num = a.get('number')
            if num and int(num) >= num_min:
                uid = ((i.get('relationships', {}) or {}).get('user', {}) or {}).get('data', {}) or {}
                uid = uid.get('id')
                txt = re.sub(r'<[^>]+>', '', a.get('contentHtml') or '')[:110]
                seen[int(num)] = (a.get('createdAt', '')[:16], users.get(uid, '?'), ug.get(uid, []), txt)
    for num in sorted(seen):
        ts, user, gr, txt = seen[num]
        print(f'  #{num} {ts} BY {user} {gr} :: {txt}')


print('\n===== 159759 ПОСТ САНЕТИ 7-Й ЧАС: КТО написал #14592+ (5 постов после 6-часового реста) =====')
d = json.load(open(os.path.join(OUT, f'discussion_159759_near999999_{CUR_TS}.json')))
a = d.get('data', {}).get('attributes', {}) or {}
print(f"  cc={a.get('commentCount')} LPN={a.get('lastPostNumber')} locked={a.get('locked')} sticky={a.get('sticky')}")
posts_after(d, 14592)

print('\n===== 196810: авторы постов после #41 (мод-реакция на наезд #35? офиц. ответ?) =====')
d810 = json.load(open(os.path.join(OUT, f'discussion_196810_near999999_{CUR_TS}.json')))
a810 = d810.get('data', {}).get('attributes', {}) or {}
print(f"  cc={a810.get('commentCount')} LPN={a810.get('lastPostNumber')}")
posts_after(d810, 42)

print('\n===== 196817 Культисты: состояние (вспух от 21?) =====')
d817 = json.load(open(os.path.join(OUT, f'discussion_196817_near999999_{CUR_TS}.json')))
a817 = d817.get('data', {}).get('attributes', {}) or {}
print(f"  cc={a817.get('commentCount')} LPN={a817.get('lastPostNumber')}")
