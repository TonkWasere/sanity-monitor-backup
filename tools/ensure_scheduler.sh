#!/bin/bash
# ensure_scheduler.sh — 54-689: гарантирует, что локальный шедулер мониторинга жив.
# ВЫЗЫВАТЬ В НАЧАЛЕ ЛЮБОГО ЧАТ-КРОН-ТИКА (после VM-рецикла шедулер мёртв — чат-агент
# единственный, кто может его поднять до следующего слота).
cd /home/z/my-project/mini-services/monitor-scheduler || exit 1
if curl -s --max-time 3 http://127.0.0.1:3031/health 2>/dev/null | grep -q '"alive":true'; then
  echo "[ensure_scheduler] жив: $(curl -s --max-time 3 http://127.0.0.1:3031/health | head -c 160)"
  exit 0
fi
echo "[ensure_scheduler] не отвечает — стартуем"
rm -f /tmp/monitor_scheduler.pid
nohup bun run dev >> scheduler.log 2>&1 &
sleep 2
if curl -s --max-time 3 http://127.0.0.1:3031/health 2>/dev/null | grep -q '"alive":true'; then
  echo "[ensure_scheduler] поднят"
  exit 0
fi
echo "[ensure_scheduler] НЕ ПОДНЯЛСЯ — смотреть scheduler.log"
exit 2
