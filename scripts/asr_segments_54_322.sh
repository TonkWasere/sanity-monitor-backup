#!/bin/bash
# Разбивка аудио на 28с-сегменты и ASR-цикл (лимит API 30с)
cd /home/z/my-project/video_tmp
rm -f seg_*.wav asr_seg_*.txt
ffmpeg -v error -i audio_16k.webm -f segment -segment_time 28 -ac 1 -ar 16000 -c:a pcm_s16le seg_%02d.wav
ls seg_*.wav | wc -l
for f in seg_*.wav; do
  out="${f%.wav}"
  timeout 60 z-ai asr -f "$f" -o "asr_${out}.json" > /dev/null 2>&1
  if [ -f "asr_${out}.json" ]; then
    python3 -c "
import json
d=json.load(open('asr_${out}.json'))
t=(d.get('text') if isinstance(d,dict) else d) or ''
open('asr_${out}.txt','w').write(t.strip())
"
    echo "$f OK"
  else
    echo "$f FAIL"
  fi
done
echo "=== СКЛЕЙКА ==="
python3 - << 'EOF'
import glob
parts = sorted(glob.glob('asr_seg_*.txt'))
full = ' '.join(open(p, encoding='utf-8').read().strip() for p in parts)
full = ' '.join(full.split())
open('transcript_full.txt', 'w', encoding='utf-8').write(full)
print('TOTAL LEN:', len(full))
print(full[:500])
EOF
