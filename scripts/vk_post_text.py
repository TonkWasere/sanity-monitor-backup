#!/usr/bin/env python3
# vk_post_text.py — вытянуть текст поста VK-стены из JS-payload снапшота
import re, html, sys

fn = sys.argv[1] if len(sys.argv) > 1 else 'output/evidence_post/ext_vk_wall_20261024_2028.html'
pid = sys.argv[2] if len(sys.argv) > 2 else '1148533'
raw = open(fn, 'rb').read().decode('utf-8', errors='ignore')

i = raw.find(pid)
if i < 0:
    print('ID not found'); sys.exit(0)
seg = raw[max(0, i - 100): i + 2500]

# VK: \uXXXX и \n внутри JSON-строк
def deesc(s):
    s = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)
    s = s.replace('\\n', ' ¶ ')
    return s

seg = deesc(seg)
# убрать теги и лишнее
txt = re.sub(r'<[^>]+>', ' ', seg)
txt = re.sub(r'\s{2,}', ' ', html.unescape(txt))
print(txt[:900])
