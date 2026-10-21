#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# analyze54_137.py — (1) вырез-линия: поснапная сверка cc/LPN 1733-vs-1833 по всем 61 ключам №178;
# (2) контент middle-окна 196799 (#40-#66, флейм 3-го часа); (3) 196810: ответы после Crios #7;
# (4) Пост Санити: подтверждение рест-состояния.
import json, os, re
from datetime import datetime, timezone

OUT = '/home/z/my-project/output/evidence_post'
PREV_TS, CUR_TS = '20261021_1733', '20261021_1833'
PREV_LPN = {191614: 7224, 196749: 40, 196755: 47, 196758: 25, 196770: 121, 196773: 91, 196777: 66, 196778: 41,
            196794: 25, 196801: 11, 196803: 20, 196804: 4, 196805: 25, 196808: 6, 196809: 26, 196810: 24,
            196811: 5, 159759: 14591, 112917: 67700, 187993: 1251, 195081: 1076, 196718: 115, 196721: 18,
            196727: 38, 196730: 32, 196732: 27, 196734: 55, 196735: 38, 196739: 13, 196742: 13, 196745: 14,
            196747: 4, 196748: 45, 196750: 13, 196752: 28, 196754: 11, 196756: 23, 196757: 1, 196760: 33,
            196761: 30, 196762: 4, 196763: 49, 196764: 11, 196765: 19, 196766: 1, 196767: 34, 196768: 8,
            196771: 16, 196772: 31, 196781: 4, 196782: 7, 196783: 13, 196784: 39, 196785: 26, 196786: 33,
            196787: 3, 196788: 45, 196791: 55, 196795: 9, 196797: 35, 196799: 39}


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
                        (a.get('user', {}) or {}).get('username') if isinstance(a.get('user'), dict) else None,
                        re.sub(r'<[^>]+>', '', a.get('contentHtml') or a.get('content') or '')[:100]))
    return res


print('===== ВЫРЕЗ-ЛИНИЯ: cc/LPN 1733-vs-1833 (вырез = cc_delta < lpn_delta) =====')
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
        print(f'  [{tid}] снап 1733 отсутствует (пропуск)')
    except Exception as e:  # noqa: BLE001
        print(f'  [{tid}] fail: {e}')
print(f'>>> подозрений: {len(susp)} {susp if susp else ""}')

print('\n===== 196799 MIDDLE-ОКНО #40-#66 (флейм 3-го часа) =====')
mid = posts_of(196799, CUR_TS, near='52')
tail = posts_of(196799, CUR_TS)
seen = {}
for num, ts, user, txt in mid + tail:
    if num and num not in seen:
        seen[num] = (ts, user, txt)
for num in sorted(k for k in seen if 40 <= k <= 66):
    ts, user, txt = seen[num]
    print(f'  #{num} {ts} :: {txt[:95]}')

print('\n===== 196810: авторы #8-#33 (офиц. ответ разработчиков? Crios после #7?) =====')
p810 = posts_of(196810, CUR_TS)
d810 = json.load(open(os.path.join(OUT, f'discussion_196810_near999999_{CUR_TS}.json')))
users = {i['id']: (i.get('attributes', {}) or {}).get('username')
         for i in (d810.get('included') or []) if i.get('type') == 'users'}
groups = {i['id']: (i.get('attributes', {}) or {}).get('nameSingular')
          for i in (d810.get('included') or []) if i.get('type') == 'groups'}
seen2 = {}
for num, ts, user, txt in p810:
    if num and num not in seen2:
        seen2[num] = (ts, user, txt)
for num in sorted(k for k in seen2 if k >= 8):
    ts, _, txt = seen2[num]
    # автор из raw
    print(f'  #{num} {ts} :: {txt[:90]}')
# кто из авторов постов с группами Рупор/Комьюнити-менеджер/Легенда писал после #7
post_users = {}
d_data = d810.get('data')
items = d_data if isinstance(d_data, list) else []
for i in items + (d810.get('included') or []):
    if isinstance(i, dict) and i.get('type') == 'posts':
        a = i.get('attributes', {}) or {}
        num = a.get('number')
        uid = ((i.get('relationships', {}) or {}).get('user', {}) or {}).get('data', {}) or {}
        uid = uid.get('id')
        if num and num >= 8 and uid:
            post_users[num] = users.get(uid, uid)
print('  авторы после #7:', {n: post_users.get(n) for n in sorted(post_users, key=lambda x: int(x))})

print('\n===== ПОСТ САНЕТИ 5-Й ЧАС: рест-состояние 159759 =====')
a = attrs(159759, CUR_TS)
print(f"  cc={a.get('commentCount')} LPN={a.get('lastPostNumber')} locked={a.get('locked')} — 5-Й ЧАС стоя (постов после #14591 нет)")
