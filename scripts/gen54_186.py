#!/usr/bin/env python3
# gen54_186.py — цепная генерация rescan54_186_fetch.py из rescan54_185_fetch.py
# Строгие REPL: каждый old обязан встретиться ровно 1 раз, иначе падаем.
import py_compile, sys

SRC = '/home/z/my-project/tools/rescan54_185_fetch.py'
DST = '/home/z/my-project/tools/rescan54_186_fetch.py'

OLD_HEADER = '''# rescan54_185_fetch.py — Task 54-185: часовой cron-раунд ~00:20 UTC 24.10
# (окно 23:20->00:20; 54-184 закрыт 23:36 коммитом af9b85d1). SNAP15-линия: 196926
# «ЩА ПОФАРМИМ» фарм-всплеск +12 (22/22 @23:40) затем выдохся +1 (23/23 @23:55, @00:10
# встал); 196927 +2 (8/8); 196931 +1 (2/2). Watch: ★ 196926 выпуск из young (>2h давно)
# — фоном умер?; ★ 196911 разбудился (85/84); 191614 гэп-62; 196889 гэп-4; канон 58-й;
# Санити 59-й; GG 35-й; ОТС 152; флешмоб 114-й; 404 94-й; ТГК пауза 11+ ч?; ВК-стена
# вернуть после анти-бота?; Crios ~28-29 ч?; PAT №59 (ротация у автора не сделана)'''

NEW_HEADER = '''# rescan54_186_fetch.py — Task 54-186: часовой cron-раунд ~01:20 UTC 24.10
# (окно 00:20->01:20; 54-185 закрыт 00:29 коммитом 9f5d6060). WIPE-11-ЗЕРКАЛО 01:12:
# ВМ снова откатилась (71c70b83 19.10) → ff-merge 9f5d6060 + vault-рекавери (sha
# 7f9edd5d = эталон 54-61, API 200,creds 600) + prev_lpn_186 восстановлена из
# git-снапов 0020. SNAP15: young x4 выпущены 00:25 (196926-929 → graduated=13);
# 196926 фарм встал (23/23). Watch: ★ 196889 OTS клиент-реквесты (+3, 72/68, гэп-4);
# ★ 196911 магазин-фидбек (87/86, ВК-зеркало 1148374); 196907 вялотёк; 191614 гэп-62;
# канон 59-й; Санити 60-й; GG 36-й; ОТС 153; флешмоб 115-й; 404 95-й; ТГК пауза 12+ ч?;
# ВК-стена стабильна после анти-бота?; PAT №60 (ротации снова нет)'''

REPL = [
    (OLD_HEADER, NEW_HEADER),
    ("TS = '20261024_0020'", "TS = '20261024_0120'"),
    ("WIN = '2026-10-23T23:20'  # окно 1 ч (54-184 закрыт 23:36)",
     "WIN = '2026-10-24T00:20'  # окно 1 ч (54-185 закрыт 00:29)"),
    ("===== LPN/CC ДЕЛЬТЫ vs prev_lpn_185 (база 23:20) =====",
     "===== LPN/CC ДЕЛЬТЫ vs prev_lpn_186 (база 00:20 — восстановлена из git после WIPE-11) ====="),
    ("prev = json.load(open('/tmp/prev_lpn_185.json'))",
     "prev = json.load(open('/tmp/prev_lpn_186.json'))"),
    ("(база prev_lpn_185: {len(prev)} ключей, 23:20 UTC — раунд 54-184)",
     "(база prev_lpn_186: {len(prev)} ключей, 00:20 UTC — раунд 54-185, восстановлена из git)"),
    ("open('/tmp/prev_lpn_186.json', 'w'))", "open('/tmp/prev_lpn_187.json', 'w'))"),
    (">>> prev_lpn_186.json сохранён", ">>> prev_lpn_187.json сохранён"),
    ("DONE 54-185 PHASE1+2", "DONE 54-186 PHASE1+2"),
]

def main():
    src = open(SRC, encoding='utf-8').read()
    for i, (old, new) in enumerate(REPL, 1):
        n = src.count(old)
        if n != 1:
            print(f'R{i} FAIL: {n} вхождений (нужно 1): {old[:60]!r}')
            return 1
        src = src.replace(old, new)
    open(DST, 'w', encoding='utf-8').write(src)
    py_compile.compile(DST, doraise=True)
    print(f'OK: {DST} сгенерирован, py_compile OK, {len(REPL)} REPL применено')
    return 0

if __name__ == '__main__':
    sys.exit(main())
