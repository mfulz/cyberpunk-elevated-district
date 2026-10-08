#!/usr/bin/env python3
"""Convert a flat binary into a TinyUF2 image with 256-byte payload blocks."""

from __future__ import annotations

import argparse
import struct
from pathlib import Path


UF2_MAGIC_START0 = 0x0A324655
UF2_MAGIC_START1 = 0x9E5D5157
UF2_MAGIC_END = 0x0AB16F30
UF2_FLAG_FAMILY_ID_PRESENT = 0x00002000
PAYLOAD_SIZE = 256
BLOCK_SIZE = 512


def integer(value: str) -> int:
    return int(value, 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--base", type=integer, required=True)
    parser.add_argument("--family", type=integer, required=True)
    args = parser.parse_args()

    binary = args.input.read_bytes()
    block_count = (len(binary) + PAYLOAD_SIZE - 1) // PAYLOAD_SIZE
    output = bytearray()

    for block_number in range(block_count):
        offset = block_number * PAYLOAD_SIZE
        payload = binary[offset : offset + PAYLOAD_SIZE]
        payload = payload.ljust(PAYLOAD_SIZE, b"\x00")
        block = bytearray(BLOCK_SIZE)
        struct.pack_into(
            "<IIIIIIII",
            block,
            0,
            UF2_MAGIC_START0,
            UF2_MAGIC_START1,
            UF2_FLAG_FAMILY_ID_PRESENT,
            args.base + offset,
            PAYLOAD_SIZE,
            block_number,
            block_count,
            args.family,
        )
        block[32 : 32 + PAYLOAD_SIZE] = payload
        struct.pack_into("<I", block, BLOCK_SIZE - 4, UF2_MAGIC_END)
        output.extend(block)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
