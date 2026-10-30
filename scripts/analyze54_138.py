#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# analyze54_138.py — (1) вырез-линия: поснапная сверка cc/LPN 1833-vs-1934 по всем 64 ключам №179;
# (2) 196810: авторы постов после Crios #33 «Зарепортил» (офиц. ответ?);
# (3) Пост Санити: рест-состояние 159759 6-й час.
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
PREV_TS, CUR_TS = '20261021_1833', '20261021_1934'
PREV_LPN = {191614: 7226, 196749: 42, 196755: 47, 196758: 25, 196770: 122, 196773: 94, 196777: 66, 196778: 41,
            196794: 25, 196801: 11, 196803: 20, 196804: 4, 196805: 28, 196808: 6, 196809: 29, 196810: 33,
            196811: 5, 196813: 12, 196815: 6, 196816: 13, 159759: 14591, 112917: 67701, 187993: 1251,
            195081: 1076, 196718: 115, 196721: 18, 196727: 38, 196730: 32, 196732: 27, 196734: 55,
            196735: 38, 196739: 13, 196742: 13, 196745: 14, 196747: 4, 196748: 45, 196750: 13, 196752: 28,
            196754: 11, 196756: 23, 196757: 1, 196760: 33, 196761: 30, 196762: 4, 196763: 49, 196764: 11,
            196765: 19, 196766: 1, 196767: 34, 196768: 8, 196771: 16, 196772: 33, 196781: 4, 196782: 7,
            196783: 13, 196784: 40, 196785: 26, 196786: 33, 196787: 3, 196788: 45, 196791: 57, 196795: 9,
            196797: 35, 196799: 66}


def attrs(tid, ts):
    fn = os.path.join(OUT, f'discussion_{tid}_near999999_{ts}.json')
    d = json.load(open(fn))
    return d.get('data', {}).get('attributes', {}) or {}


def posts_of(tid, ts, near='999999'):
    fn = os.path.join(OUT, f'discussion_{tid}_near{near}_{ts}.json')
    d = json.load(open(fn))
    items = d.get('data') if isinstance(d.get('data'), list) else []
    res = []
    for i in items + (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            a = i.get('attributes', {}) or {}
            res.append((a.get('number'), a.get('createdAt', '')[:16],
                        re.sub(r'<[^>]+>', '', a.get('contentHtml') or a.get('content') or '')[:100]))
    return res


print('===== ВЫРЕЗ-ЛИНИЯ: cc/LPN 1833-vs-1934 (вырез = cc_delta < lpn_delta) =====')
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

print('\n===== 196810: авторы #34+ (офиц. ответ разработчиков после Crios #33 «Зарепортил»?) =====')
d810 = json.load(open(os.path.join(OUT, f'discussion_196810_near999999_{CUR_TS}.json')))
users = {i['id']: (i.get('attributes', {}) or {}).get('username')
         for i in (d810.get('included') or []) if i.get('type') == 'users'}
groups = {i['id']: (i.get('attributes', {}) or {}).get('nameSingular')
          for i in (d810.get('included') or []) if i.get('type') == 'groups'}
ug = {}
for i in (d810.get('included') or []):
    if i.get('type') == 'users':
        gids = [x.get('id') for x in (i.get('relationships', {}) or {}).get('groups', {}).get('data', [])]
        ug[i['id']] = [groups.get(g, g) for g in gids]
seen = {}
for i in (d810.get('data') if isinstance(d810.get('data'), list) else []) + (d810.get('included') or []):
    if isinstance(i, dict) and i.get('type') == 'posts':
        a = i.get('attributes', {}) or {}
        num = a.get('number')
        if num and num >= 34:
            uid = ((i.get('relationships', {}) or {}).get('user', {}) or {}).get('data', {}) or {}
            uid = uid.get('id')
            txt = re.sub(r'<[^>]+>', '', a.get('contentHtml') or '')[:95]
            seen[num] = (a.get('createdAt', '')[:16], users.get(uid, '?'), ug.get(uid, []), txt)
for num in sorted(seen, key=lambda x: int(x)):
    ts, user, gr, txt = seen[num]
    print(f'  #{num} {ts} BY {user} {gr} :: {txt}')

print('\n===== ПОСТ САНЕТИ 6-Й ЧАС: рест-состояние 159759 =====')
a = attrs(159759, CUR_TS)
print(f"  cc={a.get('commentCount')} LPN={a.get('lastPostNumber')} locked={a.get('locked')} — 6-Й ЧАС стоя (постов после #14591 нет)")
