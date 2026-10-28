#!/bin/bash
# Ротация бандлов /home/z/backups: оставить 2 новейших (54-325: давление диска,
# полноразмерные бандлы ~440МБ; keep 2 = ~880МБ потолок). Поверх 54-233.
# Замена хрупкого пайплайна `ls -t | tail -n +4 | xargs -r rm -f`
# (в среде cron-агента пайплайн глотал имена — rm -f молча exit 0, бандлы копились).
# Чистый bash: без пайпов, без ls, только glob + -nt сортировка.
cd /home/z/backups || exit 0
shopt -s nullglob
files=(*.bundle)
[ ${#files[@]} -le 2 ] && { echo "ROTATE: ${#files[@]} бандлов — чисто"; exit 0; }
# сортировка по mtime, новейшие первыми (пузырёк, файлов ~5)
for ((i=0; i<${#files[@]}; i++)); do
  for ((j=i+1; j<${#files[@]}; j++)); do
    if [ "${files[$j]}" -nt "${files[$i]}" ]; then
      t=${files[$i]}; files[$i]=${files[$j]}; files[$j]=$t
    fi
  done
done
for ((i=2; i<${#files[@]}; i++)); do
  rm -v -- "${files[$i]}"
done
echo "ROTATE: оставлено 2, удалено $(( ${#files[@]} - 2 ))"
