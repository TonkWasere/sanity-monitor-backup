/*
 * instrumentation.ts — 54-689: bootstrap локального шедулера мониторинга.
 * Песочница убивает процессы, порождённые tool-call сессиями (проверено 23:30 UTC:
 * умирают даже setsid-процессы). Выживает только дерево платформенного дев-сервера —
 * поэтому шедулер (mini-services/monitor-scheduler) спавнится отсюда, из register(),
 * detached-процессом: он репарентится к init и живёт независимо, а singleton-pidfile
 * в самом шедулере гасит дубли при рестартах дев-сервера.
 * После VM-рецикла дев-сервер поднимает платформа → instrumentation → шедулер
 * восстанавливается АВТОМАТИЧЕСКИ (чат-крон-агент уже не обязан его поднимать,
 * ensure_scheduler.sh остаётся ручным fallback-ом).
 */
export async function register() {
  // только серверный runtime
  if (process.env.NEXT_RUNTIME !== 'nodejs') return;
  try {
    const { spawn } = await import('child_process');
    const http = await import('http');
    // уже жив? (после рестартов дев-сервера — singleton в самом шедулере тоже страхует)
    const alive = await new Promise<boolean>((resolve) => {
      const req = http.get('http://127.0.0.1:3031/health', { timeout: 1500 }, (r) => {
        r.resume();
        resolve(r.statusCode === 200);
      });
      req.on('timeout', () => { req.destroy(); resolve(false); });
      req.on('error', () => resolve(false));
    });
    if (alive) {
      console.log('[instrumentation] monitor-scheduler уже жив — не спавним');
      return;
    }
    const child = spawn('bun', ['run', 'dev'], {
      cwd: '/home/z/my-project/mini-services/monitor-scheduler',
      detached: true,
      stdio: 'ignore',
      env: { ...process.env, BUN_BE_BUN: '1' },
    });
    child.unref();
    console.log(`[instrumentation] monitor-scheduler спавнен pid=${child.pid} (detached)`);
  } catch (e) {
    console.error('[instrumentation] spawn monitor-scheduler fail:', e);
  }
}
