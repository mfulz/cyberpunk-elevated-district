# NeoPixel staircase firmware — 20 LED release

Final firmware for the two illuminated staircase modules: 15 lower steps plus
5 upper steps.

## Effect

- 20 addressable `WS2812`/NeoPixel-compatible LEDs
- physical chain order: pixel `0` at the top, pixel `19` at the bottom
- animation direction: bottom to top
- permanently illuminated base colour
- three-step-wide runner with softly faded edges
- three colour themes: purple/pink, blue/cyan and crimson/gold
- three normal runs per theme; the fourth run wipes in the next theme
- pixels `0` through `18`: 100% configured brightness
- pixel `19`: 50% because it sits directly below its diffuser without a spacer

## Target hardware

- WeAct BlackPill with `STM32F401CCU6`
- TinyUF2 bootloader
- application/vector address: `0x08010000`
- UF2 family ID: `0x57755a57`
- NeoPixel data output: `PA8`
- NeoPixel format: `GRB`, 800 kHz

### Wiring

```text
BlackPill PA8 --- 310 ohm --- DIN of top NeoPixel
5 V supply ----------------- NeoPixel 5 V
GND supply ----------------- NeoPixel GND + BlackPill GND
```

The bottom LED is the last LED in the data chain.

## Flashing the prebuilt image

1. Enter the TinyUF2 bootloader so the `BlackPill` mass-storage volume appears.
2. Copy `prebuilt/neopixel-stair-20-blackpill-f401cc.uf2` onto that volume.
3. The board reboots into the application automatically.

## Reproducible build

Known-good toolchain:

- Arduino CLI `1.4.1`
- STM32duino core `2.9.0`
- Adafruit NeoPixel `1.12.5`
- FQBN `STMicroelectronics:stm32:GenF4:pnum=BLACKPILL_F401CC`
- flash offset `0x10000`

From the repository root:

```bash
./firmware/neopixel-stair-20/build.sh
```

The script compiles the sketch, recreates BIN and UF2 files, validates the UF2
block metadata and payload, and verifies the ELF vector address when `readelf`
is available.

To validate only the packaged firmware:

```bash
python3 firmware/neopixel-stair-20/verify_release.py
```

## Files

```text
src/neopixel_stair_20/neopixel_stair_20.ino  frozen Arduino source
prebuilt/*.bin                               raw application image
prebuilt/*.uf2                               directly flashable TinyUF2 image
build.sh                                     complete build pipeline
verify_release.py                            independent BIN/UF2 validator
```
