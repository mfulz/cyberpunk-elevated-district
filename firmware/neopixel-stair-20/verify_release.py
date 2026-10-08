#!/usr/bin/env python3
"""Validate the packaged BIN/UF2 pair and TinyUF2 addressing metadata."""

from __future__ import annotations

import struct
from pathlib import Path


MAGIC_START0 = 0x0A324655
MAGIC_START1 = 0x9E5D5157
MAGIC_END = 0x0AB16F30
FAMILY_FLAG = 0x00002000
EXPECTED_BASE = 0x08010000
EXPECTED_FAMILY = 0x57755A57
BLOCK_SIZE = 512
PAYLOAD_SIZE = 256

HERE = Path(__file__).resolve().parent
PREBUILT = HERE / "prebuilt"
BIN = PREBUILT / "neopixel-stair-20-blackpill-f401cc.bin"
UF2 = PREBUILT / "neopixel-stair-20-blackpill-f401cc.uf2"


def main() -> None:
    binary = BIN.read_bytes()
    uf2 = UF2.read_bytes()
    if not binary:
        raise SystemExit("BIN is empty")
    if len(uf2) % BLOCK_SIZE:
        raise SystemExit("UF2 size is not a multiple of 512 bytes")

    block_count = len(uf2) // BLOCK_SIZE
    expected_blocks = (len(binary) + PAYLOAD_SIZE - 1) // PAYLOAD_SIZE
    if block_count != expected_blocks:
        raise SystemExit(
            f"UF2 block count mismatch: {block_count} != {expected_blocks}"
        )

    recovered = bytearray()
    for index in range(block_count):
        block = uf2[index * BLOCK_SIZE : (index + 1) * BLOCK_SIZE]
        (
            magic0,
            magic1,
            flags,
            address,
            payload_size,
            block_number,
            declared_count,
            family,
        ) = struct.unpack_from("<IIIIIIII", block, 0)
        magic_end = struct.unpack_from("<I", block, BLOCK_SIZE - 4)[0]

        expected_address = EXPECTED_BASE + index * PAYLOAD_SIZE
        checks = {
            "start magic 0": (magic0, MAGIC_START0),
            "start magic 1": (magic1, MAGIC_START1),
            "end magic": (magic_end, MAGIC_END),
            "family flag": (flags & FAMILY_FLAG, FAMILY_FLAG),
            "target address": (address, expected_address),
            "payload size": (payload_size, PAYLOAD_SIZE),
            "block number": (block_number, index),
            "declared block count": (declared_count, block_count),
            "family ID": (family, EXPECTED_FAMILY),
        }
        for label, (actual, expected) in checks.items():
            if actual != expected:
                raise SystemExit(
                    f"Block {index}: {label} mismatch: "
                    f"0x{actual:x} != 0x{expected:x}"
                )
        recovered.extend(block[32 : 32 + PAYLOAD_SIZE])

    if recovered[: len(binary)] != binary:
        raise SystemExit("UF2 payload does not reproduce the packaged BIN")
    if any(recovered[len(binary) :]):
        raise SystemExit("UF2 padding after the BIN payload is not zero")

    print(
        f"OK: {len(binary)}-byte BIN, {block_count} UF2 blocks, "
        f"base=0x{EXPECTED_BASE:08x}, family=0x{EXPECTED_FAMILY:08x}"
    )


if __name__ == "__main__":
    main()

