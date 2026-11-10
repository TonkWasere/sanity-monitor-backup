import { bootMonitorScheduler } from '@/lib/monitor_boot';

/**
 * MonitorBoot — серверный компонент-сиделка (54-689).
 * Рендерится в корневом layout при каждом SSR-запросе; платформенный поллер
 * непрерывно бьёт GET /, поэтому мёртвый шедулер поднимается за секунды.
 * Ничего не рендерит (null) — чисто серверный сайд-эффект.
 */
export default async function MonitorBoot() {
  await bootMonitorScheduler();
  return null;
}
