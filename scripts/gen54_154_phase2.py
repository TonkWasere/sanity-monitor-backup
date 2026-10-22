# gen54_154_phase2.py — фаза-2 для 54-154: rescan54_153b_phase2.py -> rescan54_154b_phase2.py
# NEW окна = 196839 (cc 1->11 взрыв); авторства дельт 1130; TS 1030->1130.
import re, py_compile

SRC = '/home/z/my-project/scripts/rescan54_153b_phase2.py'
DST = '/home/z/my-project/scripts/rescan54_154b_phase2.py'

txt = open(SRC, encoding='utf-8').read()
orig = txt

edits = [
    ("TS = '20261022_1030'", "TS = '20261022_1130'", 1),
    ("# ---- 1) NEW d/196837: OP near=1 + near999999 (createdAt ВСЕГДА, урок 54-69) ----\nfor tid in (196837,):",
     "# ---- 1) NEW d/196839: OP near=1 + near999999 (createdAt ВСЕГДА, урок 54-69) ----\nfor tid in (196839,):", 1),
    ("print('== Авторства дельт (снапы 1030) ==')\nfor tid, n in ((196806, 8), (191614, 6), (196799, 6), (196829, 4), (196832, 4), (196763, 3), (196786, 3), (196797, 3), (196828, 2), (196827, 2), (196755, 2), (196805, 2), (196809, 2), (196765, 2), (196767, 2), (196784, 2)):",
     "print('== Авторства дельт (снапы 1130) ==')\nfor tid, n in ((196832, 8), (196799, 10), (196839, 8), (196838, 3), (196837, 6), (196836, 4), (196814, 4), (196770, 4), (196795, 3), (196805, 2), (196772, 2), (196784, 2), (196806, 4), (191614, 4), (196829, 3), (112917, 2)):", 1),
    ("(159759, 196806, 196829, 196832, 196830, 196799, 196411, 196837)",
     "(159759, 196806, 196829, 196832, 196830, 196799, 196411, 196837, 196838, 196839, 196836)", 1),
    ("scripts/scan54_153_run1.log", "scripts/scan54_154_run1.log", 1),
    ("'task': '54-153', 'ts': TS, 'window': '09:30-10:30 UTC 22.10 (штатный час после WIPE-9 восстановления; замер 10:30-10:4x)',",
     "'task': '54-154', 'ts': TS, 'window': '10:30-11:30 UTC 22.10 (штатный час; после 54-153b — АРЕНА МИТРОПОЛИТА 196838 + TG 3225 11:00; замер 11:30-11:4x)',", 1),
    ("'fail_note': '404-контроли штатные: 196707/196717 (62-й час), 196796 (возврат-контроль 17-й час)',\n             'round_streak': '25-Й EXIT=0 ПОДРЯД'},",
     "'fail_note': '404-контроли штатные: 196707/196717 (63-й час), 196796 (возврат-контроль 18-й час)',\n             'round_streak': '26-Й EXIT=0 ПОДРЯД'},", 1),
    ("'wipe9_note': 'диск откатился к 19.10 23:27 (HEAD 71c70b8) — ff-merge до c9784ec + MEGA creds (sha256 = эталон), потерь НЕТ',",
     "'context_note': '54-153b: АРЕНА МИТРОПОЛИТА — 196838 (OP Girodjet 10:27:39, ОФФ ожил) + TG stalzone 3225 11:00:21 (❤148); WIPE-9-зеркало второй ВМ закрыто (ff-merge + vault sha256 = эталон); 196839 NEW-взрыв cc 1->11',", 1),
    ("'new_threads': {'op_196837': res.get('op_196837'), 'tail_196837': res.get('tail_196837')},",
     "'new_threads': {'op_196839': res.get('op_196839'), 'tail_196839': res.get('tail_196839')},", 1),
    ("check54_153b_summary.json", "check54_154b_summary.json", 1),
]

for old, new, cnt in edits:
    n = txt.count(old)
    assert n == cnt, f'ANCHOR FAIL ({n} != {cnt}): {old[:80]}'
    txt = txt.replace(old, new)

assert txt != orig
open(DST, 'w', encoding='utf-8').write(txt)
py_compile.compile(DST, doraise=True)
print(f'OK gen54_154_phase2 -> rescan54_154b_phase2.py ({len(txt)}B, py_compile OK)')
