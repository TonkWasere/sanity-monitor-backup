#!/usr/bin/env python3
# 54-327: верификационный ASR-проход видео SNATERPaAbM (вопрос автора о точности разбора)
# Метод: третья независимая сетка (сдвиг +7с, сегменты 28с) -> z-ai ASR с ретраями.
# Каждая реплика должна целиком попасть хотя бы в одну из 3 сеток (29с main / 28с seg / +7с эта).
import subprocess, json, os, time, glob, sys

os.chdir('/home/z/my-project/video_tmp')
OFF, SEG, DUR = 7.0, 28.0, 420.97
plan = []
a = OFF
while a < DUR - 1.0:
    b = min(a + SEG, DUR)
    plan.append((a, b))
    a = b
print(f'PLAN: {len(plan)} сегментов (сдвиг +{OFF}с)')

results = {}
for i, (a, b) in enumerate(plan):
    name = f'v3_{i:02d}'
    wav = f'{name}.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-to', str(b),
                    '-i', 'audio_16k.wav', '-c:a', 'pcm_s16le', wav], check=True)
    ok = False
    for attempt in range(4):
        r = subprocess.run(['timeout', '60', 'z-ai', 'asr', '-f', wav, '-o', f'{name}.json'],
                           capture_output=True, text=True)
        if os.path.exists(f'{name}.json'):
            try:
                d = json.load(open(f'{name}.json'))
                t = (d.get('text') if isinstance(d, dict) else d) or ''
                open(f'{name}.txt', 'w', encoding='utf-8').write(str(t).strip())
                results[i] = (a, b, str(t).strip())
                print(f'[{i:02d}] {a:6.1f}-{b:6.1f} OK ({len(t)} симв)')
                ok = True
                break
            except Exception as e:
                print(f'[{i:02d}] json error: {e}')
        code = r.returncode
        print(f'[{i:02d}] попытка {attempt+1} fail (rc={code}), пауза {8*(attempt+1)}с')
        time.sleep(8 * (attempt + 1))
    if not ok:
        results[i] = (a, b, '[ПРОПУСК — все попытки исчерпаны]')
        print(f'[{i:02d}] НЕ УДАЛОСЬ')
    time.sleep(2.0)

# склейка
merged = []
for i in sorted(results):
    a, b, t = results[i]
    merged.append(f'[{int(a//60):02d}:{int(a%60):02d}-{int(b//60):02d}:{int(b%60):02d}] {t}')
full = ' '.join(results[i][2] for i in sorted(results))
open('transcript_v3_shift7.txt', 'w', encoding='utf-8').write(full)
open('transcript_v3_shift7_indexed.txt', 'w', encoding='utf-8').write('\n'.join(merged) + '\n')
print('MERGED LEN:', len(full))
print('DONE v3')
