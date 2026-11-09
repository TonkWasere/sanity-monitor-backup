# cron_lock.py — 09.11.2026 fix: взаимное исключение крон-линий мониторинга (flock).
# Инцидент: восстановительный s15 18:58 (R2+R1 после WIPE-#60, тянулся до 19:03:25)
# наложился на старт LONG30 19:02:00 → вторая сессия получила мёртвую песочницу.
# Диагноз автора: «наложение выполнения одного Сканана на другой Крон-таск» —
# подтверждено метками: evidence s15 писался в 19:02:47-50 ПОСЛЕ старта LONG30.
# Механизм: эксклюзивный flock на /tmp/monitor_cron.lock (VM-локальный файл;
# ядро снимает лок при ЛЮБОМ выходе/крэше процесса — стейл-локов не бывает).
# Приоритет автора (Long30 > Snap35 > Snap15):
#   - counter_sweep (long30): ждать до 120 с (линия с приоритетом);
#   - snapnew35 (snap35) / snap15_young (snap15): мгновенный отказ, exit 3 →
#     lite-агент по выводу '>>> [SKIP-overlap]' пишет [SKIP] в worklog (протокол 2a).
# Использование в скрипте-линии:
#   from cron_lock import acquire_or_skip
#   _lk = acquire_or_skip('snap15', wait=0)
#   if _lk is None:
#       sys.exit(3)
import fcntl, time

LOCK_PATH = '/tmp/monitor_cron.lock'


def acquire_or_skip(name, wait=0):
    """Возвращает файл-хендл лока или None (занято).

    wait>0 — ждать до N секунд (приоритетная линия LONG30).
    Лок освобождается автоматически при завершении процесса (flock).
    """
    lf = open(LOCK_PATH, 'w')
    deadline = time.time() + wait
    while True:
        try:
            fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
            lf.write(name + '\n')
            lf.flush()
            return lf
        except BlockingIOError:
            if time.time() >= deadline:
                print(f'>>> [SKIP-overlap] лок занят ({name}, wait={wait}s) — быстрый выход без побочных эффектов')
                return None
            time.sleep(1)
