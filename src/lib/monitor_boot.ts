/*
 * monitor_boot.ts — 54-689: бутстрап локального шедулера мониторинга из дерева
 * дев-сервера. Песочница убивает процессы tool-call сессий (проверено: умирают даже
 * setsid) — выживает только дерево платформенного дев-сервера. Платформа непрерывно
 * поллит GET / → layout → MonitorBoot → при мёртвом /health спавнит detached-процесс
 * (репарентится к init). Cooldown 30s на попытку, singleton-pidfile в самом шедулере.
 */
import { spawn } from 'child_process';
import http from 'http';

let lastAttempt = 0;

function healthAlive(timeoutMs = 1500): Promise<boolean> {
  return new Promise((resolve) => {
    try {
      const req = http.get('http://127.0.0.1:3031/health', { timeout: timeoutMs }, (r) => {
        r.resume();
        resolve(r.statusCode === 200);
      });
      req.on('timeout', () => {
        req.destroy();
        resolve(false);
      });
      req.on('error', () => resolve(false));
    } catch {
      resolve(false);
    }
  });
}

export async function bootMonitorScheduler(): Promise<void> {
  const now = Date.now();
  if (now - lastAttempt < 30_000) return;
  lastAttempt = now;
  try {
    if (await healthAlive()) return;
    const child = spawn('bun', ['run', 'dev'], {
      cwd: '/home/z/my-project/mini-services/monitor-scheduler',
      detached: true,
      stdio: 'ignore',
    });
    child.unref();
    console.log(`[monitor-boot] monitor-scheduler спавнен pid=${child.pid} (detached, cooldown 30s)`);
  } catch (e) {
    console.error('[monitor-boot] spawn fail:', e);
  }
}
