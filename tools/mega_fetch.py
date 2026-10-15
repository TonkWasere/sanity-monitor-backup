#!/usr/bin/env python3
"""Скачивание публичного файла MEGA (Task 51-a, восстановление после отката ВМ №2)."""
import sys, os
from mega import Mega

url = "https://mega.nz/file/n5QmRLaJ#Slg7s5G7J2TH8xWfwVZxVxSh6XhTPE7XJ00eQHGcnd4"
dest = sys.argv[1] if len(sys.argv) > 1 else "/tmp/mega_restore"
os.makedirs(dest, exist_ok=True)

m = Mega()
print("start download...", flush=True)
path = m.download_url(url, dest_path=dest)
size = os.path.getsize(path)
print(f"DONE: {path}")
print(f"SIZE: {size}")
