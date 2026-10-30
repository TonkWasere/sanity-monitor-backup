#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Кадры из видео через cv2 (быстрый seek), контактные листы + отдельные ключевые кадры."""
import cv2
import numpy as np
import os

SRC = '/home/z/my-project/video_tmp/stalzone_event_arena_20261028.mp4'
OUT = '/home/z/my-project/video_tmp'
cap = cv2.VideoCapture(SRC)
fps = cap.get(cv2.CAP_PROP_FPS) or 60.0
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
dur = n / fps if fps else 0
print(f'fps={fps:.1f} frames={n} dur={dur:.1f}s')

def grab(t):
    """Кадр на секунде t (или None)."""
    idx = min(int(t * fps), n - 1)
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ok, fr = cap.read()
    return fr if ok else None

def tile(frames, cols):
    rows = (len(frames) + cols - 1) // cols
    h, w = frames[0].shape[:2]
    grid = np.full((rows * h, cols * w, 3), 24, np.uint8)
    for i, fr in enumerate(frames):
        r, c = divmod(i, cols)
        grid[r * h:r * h + h, c * w:c * w + w] = fr
    return grid

# 1) Лист из 28 кадров (каждые 15с), таймкод на кадре
step = 15.0
ts = [t for t in np.arange(5, dur - 2, step)][:28]
frames = []
for t in ts:
    fr = grab(float(t))
    if fr is None:
        continue
    fr = cv2.resize(fr, (480, 270))
    cv2.putText(fr, f'{int(t//60)}:{int(t%60):02d}', (8, 22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    frames.append(fr)
grid = tile(frames, 4)
cv2.imwrite(os.path.join(OUT, 'contact_15s.png'), grid)
print('contact_15s.png:', grid.shape, len(frames), 'кадров')

# 2) Крупные ключевые кадры: начало, треть, середина, две трети, финал
big_ts = [float(dur * f) for f in (0.03, 0.25, 0.5, 0.75, 0.97)]
big_frames = []
for t in big_ts:
    fr = grab(t)
    if fr is None:
        continue
    fr = cv2.resize(fr, (640, 360))
    cv2.putText(fr, f'{int(t//60)}:{int(t%60):02d}', (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    big_frames.append(fr)
grid2 = tile(big_frames, 3)
cv2.imwrite(os.path.join(OUT, 'contact_big5.png'), grid2)
print('contact_big5.png:', grid2.shape, len(big_frames), 'кадров')
cap.release()
