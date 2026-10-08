#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd -- "$HERE/../.." && pwd)"
SKETCH="$HERE/src/neopixel_stair_20"
OUTPUT="$HERE/prebuilt"
FQBN='STMicroelectronics:stm32:GenF4:pnum=BLACKPILL_F401CC'
UF2_BASE='0x08010000'
UF2_FAMILY='0x57755a57'

command -v arduino-cli >/dev/null || {
    echo 'arduino-cli is required' >&2
    exit 1
}

BUILD_DIR="$(mktemp -d)"
trap 'rm -rf -- "$BUILD_DIR"' EXIT

arduino-cli compile \
    --fqbn "$FQBN" \
    --build-property 'build.flash_offset=0x10000' \
    --output-dir "$BUILD_DIR" \
    "$SKETCH"

mkdir -p "$OUTPUT"
cp "$BUILD_DIR/neopixel_stair_20.ino.bin" \
   "$OUTPUT/neopixel-stair-20-blackpill-f401cc.bin"

python3 "$ROOT/tools/bin_to_uf2.py" \
    "$OUTPUT/neopixel-stair-20-blackpill-f401cc.bin" \
    "$OUTPUT/neopixel-stair-20-blackpill-f401cc.uf2" \
    --base "$UF2_BASE" \
    --family "$UF2_FAMILY"

python3 "$HERE/verify_release.py"

if command -v readelf >/dev/null; then
    vector_address="$({ readelf -SW "$BUILD_DIR/neopixel_stair_20.ino.elf" || true; } \
        | sed -n 's/.*\.isr_vector[[:space:]]\+PROGBITS[[:space:]]\+\([0-9A-Fa-f]\+\).*/\1/p' \
        | head -n 1)"
    if [[ "$vector_address" != '08010000' ]]; then
        echo "Unexpected vector address: ${vector_address:-not found}" >&2
        exit 1
    fi
    echo 'ELF vector address: 0x08010000'
fi

sha256sum \
    "$SKETCH/neopixel_stair_20.ino" \
    "$OUTPUT/neopixel-stair-20-blackpill-f401cc.bin" \
    "$OUTPUT/neopixel-stair-20-blackpill-f401cc.uf2"
