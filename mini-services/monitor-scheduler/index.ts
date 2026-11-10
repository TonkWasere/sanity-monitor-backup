// mini-services/monitor-scheduler/index.ts — 54-689: локальный автономный шедулер
// трёх линий мониторинга STALCRAFT-форума (fallback при отказе/рецикле чат-кронов).
//
// Слоты (UTC): long30 :02/:32 — свип диапазона; s15 :13/:28/:43/:58 — молодые треды;
// s35 :21 — снап новых тредов. Запуск через +90с после слота: чат-крон-агент получает
// приоритет, коллизии гасит flock в самих скриптах (s15/s35 → [SKIP-overlap]).
// Каждый тик: python3 tools/auto_tick.py <line> — полный цикл lite-агента
// (self-heal R2/R1 → линия → ledger/worklog → commit → dual push → бандл → инвариант).
//
// Health: http://127.0.0.1:3031/health — JSON (alive, pid, busy, последние тики).
// Singleton: /tmp/monitor_scheduler.pid (свой pid — не считается чужим, для bun --hot).
const PORT = 3031;
const REPO = '/home/z/my-project';
const PIDFILE = '/tmp/monitor_scheduler.pid';
const LOG = `${REPO}/mini-services/monitor-scheduler/scheduler.log`;

import { existsSync, readFileSync, writeFileSync, appendFileSync } from 'fs';

const STARTED = new Date().toISOString();

function log(msg: string) {
  // Файловый лог: шедулер спавнится с stdio:'ignore' (MonitorBoot) — console.log теряется.
  try { appendFileSync(LOG, `${new Date().toISOString()} ${msg}\n`); } catch {}
}

// --- singleton (учитываем bun --hot: свой pid в pidfile не блокирует) ---
try {
  if (existsSync(PIDFILE)) {
    const old = parseInt(readFileSync(PIDFILE, 'utf8').trim() || '0');
    if (old && old !== process.pid) {
      try {
        process.kill(old, 0);
        console.log(`monitor-scheduler already running pid=${old} — выходим`);
        process.exit(0);
      } catch { /* stale pidfile */ }
    }
  }
} catch {}
try { writeFileSync(PIDFILE, String(process.pid)); } catch {}

log(`monitor-scheduler started pid=${process.pid} port=${PORT} (host: ${process.env.PPIDS ? 'dev-server' : 'external'})`);

type TickInfo = { ts: string; rc: number | null; dur?: number; note?: string };
const state: Record<string, TickInfo> = {};
const fired = new Set<string>();
const SLOTS: Record<string, number[]> = { long30: [2, 32], s15: [13, 28, 43, 58], s35: [21] };
const DELAY_MS = 90_000;
const TIMEOUT_MS: Record<string, number> = { long30: 14 * 60_000, s15: 7 * 60_000, s35: 7 * 60_000 };
let busy = false;

function spawnTick(line: string) {
  if (busy) { log(`SKIP ${line}: предыдущий тик ещё работает`); return; }
  busy = true;
  const started = new Date().toISOString();
  log(`START ${line}`);
  let p: Bun.Subprocess;
  try {
    // NB: Bun.spawn НЕ принимает stderr:'stdout' (Node-семантика) — авто-тик сам
    // пишет свои логи в /tmp/auto_tick_last_<line>.log, здесь stdio можно глушить
    p = Bun.spawn(['python3', `${REPO}/tools/auto_tick.py`, line], {
      cwd: REPO, stdout: 'ignore', stderr: 'ignore',
    });
  } catch (e) {
    busy = false;
    log(`SPAWN-FAIL ${line}: ${e}`);
    return;
  }
  const timer = setTimeout(() => {
    try { p.kill(); log(`TIMEOUT ${line} — убит по лимиту`); } catch {}
  }, TIMEOUT_MS[line]);
  p.exited.then((rc) => {
    clearTimeout(timer);
    busy = false;
    const dur = Math.round((Date.now() - Date.parse(started)) / 1000);
    state[line] = { ts: started, rc, dur };
    log(`DONE ${line} rc=${rc} dur=${dur}s`);
  });
}

// --- планировщик: каждые 20с сверяем стеночные слоты (UTC) ---
setInterval(() => {
  if (busy) return;
  const now = new Date();
  const h = now.getUTCHours(), m = now.getUTCMinutes();
  const dayKey = `${now.getUTCFullYear()}-${now.getUTCMonth()}-${now.getUTCDate()}`;
  for (const [line, mins] of Object.entries(SLOTS)) {
    for (const mm of mins) {
      const id = `${dayKey}:${line}:${h}:${mm}`;
      if (fired.has(id)) continue;
      const slotMs = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), h, mm) + DELAY_MS;
      const age = Date.now() - slotMs;
      if (age >= 0 && age < 5 * 60_000) {   // не старше 5 мин (после сна/лагов не стреляем в прошлое)
        fired.add(id);
        spawnTick(line);
      }
    }
  }
}, 20_000);

process.on('uncaughtException', (e) => {
  log(`FATAL uncaughtException: ${e?.stack || e}`);
  process.exit(1);
});
process.on('unhandledRejection', (e) => {
  log(`FATAL unhandledRejection: ${e}`);
  process.exit(1);
});

Bun.serve({
  port: PORT,
  fetch(req) {
    const u = new URL(req.url);
    if (u.pathname === '/health') {
      return Response.json({
        alive: true, pid: process.pid, started_at: STARTED, busy,
        slots: SLOTS, delay_s: DELAY_MS / 1000, ticks: state,
      });
    }
    return new Response('monitor-scheduler alive; see /health\n');
  },
});
log(`health endpoint bound on :${PORT}`);
