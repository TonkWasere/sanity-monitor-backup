#!/usr/bin/env python3
"""
mega_pull.py — скачивание и расшифровка публичных ссылок MEGA (/file/ формат).

Схема (восстановлена из megajs + meganz/sdk 18.10.2026, раунд 54-60-MEGA):
  - ключ ссылки 43 симв. base64url = 32 байта
  - AES-128 ключ = XOR(key[:16], key[16:32])           (unmergeKeyMac)
  - attrs: AES-CBC(iv=0), формат "MEGA{...}" JSON
  - контент: AES-128-CTR, nonce = key[16:24], счётчик с 0
    (счётчик-блок = nonce || pos/16 — позади nonce, инкремент от конца)
  - MAC: CBC-MAC iv=nonce||nonce, condense (fold 16->8), сверка с key[24:32]

Использование:
  python3 tools/mega_pull.py <mega_url> [output_path]
Если output не задан — имя берётся из attrs и файл пишется в /tmp/<name>.

Заметка API: download-URL выдаётся только при {"a":"g","g":1,"p":<id>,"ssl":2};
URL одноразовый/короткоживущий — качать сразу. При 403 — перезапросить.
"""
import base64
import json
import struct
import sys
import time
import urllib.request
from pathlib import Path

from Crypto.Cipher import AES

API = "https://g.api.mega.co.nz/cs"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"


def b64d(s: str) -> bytes:
    s = s.replace("-", "+").replace("_", "/")
    return base64.b64decode(s + "=" * (-len(s) % 4))


def api_call(payload: dict, file_id: str) -> dict:
    req = urllib.request.Request(
        f"{API}?id=1&n={file_id}",
        data=json.dumps([payload]).encode(),
        headers={"User-Agent": UA, "Content-Type": "application/json"},
    )
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode())


def get_info(file_id: str, retries: int = 5) -> dict:
    for attempt in range(retries):
        r = api_call({"a": "g", "g": 1, "p": file_id, "ssl": 2}, file_id)
        if isinstance(r[0], dict) and "g" in r[0]:
            return r[0]
        time.sleep(4 + attempt * 2)
    raise RuntimeError(f"MEGA не выдал download-URL: {json.dumps(r)[:200]}")


def cbc_mac(k: bytes, data: bytes, nonce: bytes) -> bytes:
    """megajs MAC: per-block CBC с iv=nonce||nonce, затем condense:
    ещё ОДИН ecb-шифр результата, потом fold 16->8 (w0^w1, w2^w3)."""
    e = AES.new(k, AES.MODE_ECB)
    mac = nonce + nonce
    for p in range(0, len(data), 16):
        block = data[p:p + 16].ljust(16, b"\0")
        mac = bytes(a ^ b for a, b in zip(mac, block))
        mac = e.encrypt(mac)
    mac = e.encrypt(mac)  # condense: extra ECB encrypt
    return struct.pack(
        ">II",
        struct.unpack(">I", mac[0:4])[0] ^ struct.unpack(">I", mac[4:8])[0],
        struct.unpack(">I", mac[8:12])[0] ^ struct.unpack(">I", mac[12:16])[0],
    )


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    url = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None

    file_id = url.split("/file/")[1].split("#")[0]
    key = b64d(url.split("#")[1])
    if len(key) != 32:
        print(f"ОШИБКА: ключ {len(key)}B — ожидался 32B (новый /file/ формат)")
        return 1

    k = bytes(a ^ b for a, b in zip(key[:16], key[16:32]))
    nonce, expected_mac = key[16:24], key[24:32]

    info = get_info(file_id)
    size, url_dl = info["s"], info["g"]
    print(f"[mega] файл: size={size} B")

    attrs = None
    if "at" in info:
        dec = AES.new(k, AES.MODE_CBC, b"\0" * 16).decrypt(b64d(info["at"]))
        dec = dec.rstrip(b"\0")
        if dec.startswith(b"MEGA{"):
            attrs = json.loads(dec[4:].decode())
            print(f"[mega] имя: {attrs.get('n')!r}  fingerprint: {attrs.get('c', '?')}")
    if out_path is None:
        out_path = f"/tmp/{(attrs or {}).get('n', file_id)}"

    blob = urllib.request.urlopen(
        urllib.request.Request(url_dl, headers={"User-Agent": UA}), timeout=120
    ).read()
    if len(blob) < size:
        raise RuntimeError(f"скачано {len(blob)} < {size}")
    print(f"[mega] скачано {len(blob)} B")

    pt = AES.new(k, AES.MODE_CTR, nonce=nonce, initial_value=0).decrypt(blob)[:size]

    mac = cbc_mac(k, pt, nonce)
    ok = mac == expected_mac
    print(f"[mega] MAC: {'OK — целостность подтверждена' if ok else 'MISMATCH — данные повреждены!'}")
    if not ok:
        return 1

    # MEGA-паддинг: хвостовые нули + последний байт = длина паддинга
    clean = pt.rstrip(b"\0")
    if clean and clean[-1] <= 16:
        clean = clean[:-clean[-1]]
    Path(out_path).write_bytes(clean)
    print(f"[mega] сохранено: {out_path} ({len(clean)} B чистых из {len(pt)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
