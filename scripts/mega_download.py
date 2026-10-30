#!/usr/bin/env python3
"""MEGA file link downloader (direct API, no external deps beyond pycryptodome).

Usage: python3 mega_download.py <mega_link> <out_dir>
Link format: https://mega.nz/file/<HANDLE>#<KEY22>
Downloads file metadata, encrypted payload, decrypts (AES-128-CBC, IV=0),
writes to out_dir using the real filename from encrypted attributes.
"""
import base64
import json
import os
import random
import string
import sys

import requests
from Crypto.Cipher import AES
from Crypto.Util import Counter

API = "https://g.api.mega.co.nz/cs"


def b64_to_bytes(s: str) -> bytes:
    s = s.replace("-", "+").replace("_", "/")
    s += "=" * ((4 - len(s) % 4) % 4)
    return base64.b64decode(s)


def handle_and_key(link: str):
    link = link.rstrip("/")
    if "/file/" in link:
        frag = link.split("/file/", 1)[1]
    elif "/#!" in link:
        frag = link.split("/#!", 1)[1]
    else:
        raise SystemExit("unsupported link format")
    if "#" not in frag:
        raise SystemExit("no key fragment")
    handle, key = frag.split("#", 1)
    return handle, key


def main():
    link, out_dir = sys.argv[1], sys.argv[2]
    handle, key_b64 = handle_and_key(link)
    key = b64_to_bytes(key_b64)
    print(f"handle={handle} key_bytes={len(key)}")

    sid = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    body = [{"a": "g", "p": handle}]
    r = requests.post(f"{API}?id=0&n={sid}", data=json.dumps(body), timeout=30)
    r.raise_for_status()
    resp = r.json()
    if isinstance(resp, int):
        raise SystemExit(f"API error code {resp}")
    meta = resp[0]
    size = meta["s"]
    dl_url = meta.get("g")
    at_b64 = meta.get("at")
    print(f"size={size} bytes ({size/1048576:.1f} MiB) url={'yes' if dl_url else 'no'}")

    # decrypt attributes for filename
    name = f"mega_{handle}.bin"
    if at_b64:
        try:
            at = b64_to_bytes(at_b64)
            cipher = AES.new(key, AES.MODE_CBC, b"\0" * 16)
            dec = cipher.decrypt(at)
            # first byte block: length prefix (megacrypto attr format)
            if dec[0] == 2:  # new format: next 8 bytes little-endian length, then JSON
                alen = int.from_bytes(dec[1:9], "little")
                attrs = json.loads(dec[9:9 + alen])
            else:  # old format: 8-byte length prefix
                alen = int.from_bytes(dec[:8], "little")
                attrs = json.loads(dec[8:8 + alen])
            name = attrs.get("n", name)
            print(f"filename={name!r}")
        except Exception as e:
            print(f"attr decode failed ({e}), fallback name")

    if not dl_url:
        raise SystemExit("no download URL in metadata")

    out_path = os.path.join(out_dir, name)
    if os.path.exists(out_path) and os.path.getsize(out_path) == size:
        print(f"already downloaded: {out_path}")
    else:
        print(f"downloading -> {out_path} ...")
        with requests.get(dl_url, stream=True, timeout=120) as resp:
            resp.raise_for_status()
            tmp = out_path + ".part"
            enc_len = size + (-size % 16)  # pad to AES block
            done = 0
            with open(tmp, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1024 * 512):
                    f.write(chunk)
                    done += len(chunk)
        print("download done")

        # decrypt whole file: AES-128-CBC IV=0 (counter-based per MEGA spec)
        k = key[:16]
        ctr = Counter.new(128, initial_value=0)
        cipher = AES.new(k, AES.MODE_CTR, counter=ctr)
        with open(tmp, "rb") as f:
            enc = f.read()
        dec = cipher.decrypt(enc[:enc_len])[:size]
        with open(out_path, "wb") as f:
            f.write(dec)
        os.remove(tmp)
        print(f"decrypted {len(dec)} bytes")

    print(f"OK {out_path} ({os.path.getsize(out_path)} bytes)")


if __name__ == "__main__":
    main()
