#!/usr/bin/env python3
# restore_state_from_repo.py — Хранилище состояния (54-211-B, прямая задача автора
# после WIPE-29: «Хранилище в гит-репо, и с него в случае чего таскать»).
#
# Проблема: /tmp/prev_lpn_*.json гибнут при каждом откате ВМ (29 подтверждений),
# каждый раз нужен rebuild из снапов + контрольная таблица.
# Решение: часовой раунд после обхода копирует свежайший /tmp/prev_lpn_<N>.json
# в output/08_monitoring/state_snapshots/ (git-tracked → вайпо-иммунно).
# Этот скрипт — обратная сторона: мгновенное восстановление /tmp из репо.
# rebuild_prev_lpn_*.py остаются fallback-ом (когда снапшот старее нужного N).
#
# Использование: python3 tools/restore_state_from_repo.py [--all]
#   (по умолчанию — только максимальный N; --all — все найденные снапшоты)
import json, os, glob, shutil, sys

SNAP_DIR = '/home/z/my-project/output/08_monitoring/state_snapshots'
TMP = '/tmp'

def snap_num(path):
    base = os.path.basename(path)
    try:
        return int(base.replace('prev_lpn_', '').replace('.json', ''))
    except ValueError:
        return -1

def main():
    snaps = sorted(glob.glob(os.path.join(SNAP_DIR, 'prev_lpn_*.json')), key=snap_num)
    if not snaps:
        print('>>> state_snapshots пуст — Хранилище недоступно, fallback: rebuild_prev_lpn_*.py')
        return 1
    targets = snaps if '--all' in sys.argv else [snaps[-1]]
    restored = 0
    for snap in targets:
        n = snap_num(snap)
        dst = os.path.join(TMP, f'prev_lpn_{n}.json')
        try:
            d = json.load(open(snap))
            keys = len(d)
            if keys == 0:
                print(f'  SKIP prev_lpn_{n}.json: 0 ключей (битый снапшот)')
                continue
            shutil.copyfile(snap, dst)
            os.chmod(dst, 0o600)
            src_exists = os.path.exists(os.path.join(TMP, f'prev_lpn_{n}.json'))
            print(f'>>> prev_lpn_{n}.json восстановлен из Хранилища: {keys} ключей -> {dst}'
                  + (' (перезаписал /tmp-версию)' if src_exists else ''))
            restored += 1
        except Exception as e:
            print(f'  FAIL prev_lpn_{n}.json: {e}')
    print(f'>>> готово: восстановлено {restored}/{len(targets)}; '
          f'доступные снапшоты: {[snap_num(s) for s in snaps]}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
