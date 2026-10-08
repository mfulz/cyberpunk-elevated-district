# Electronics and power distribution

The electronics box combines the 20-pixel staircase controller and a fixed 5 V
star distributor for the illuminated buildings.

## Important interface limitation

The USB-C connectors in this project are **power-only fixed-5-V connectors**.
They are not standards-compliant general-purpose USB-C/USB-PD ports.

- Supply the box with regulated 5 V only.
- Do not connect laptops, phones or arbitrary USB-C equipment.
- Never inject a negotiated 9, 12, 15 or 20 V profile into this bus.
- Simple breakout boards are not dimensionally or electrically standardized;
  inspect their CC implementation before relying on a USB-C-to-C source.

## System topology

```text
regulated 5 V input
        |
        +---- 5 V/GND star ---- USB-C power output 1 ---- building
        |                   +--- USB-C power output 2 ---- building
        |                   +--- USB-C power output 3 ---- building
        |                   +--- USB-C power output 4 ---- building
        |                   `--- USB-C power output 5 ---- building
        |
        +---- BlackPill 5 V input
        |
        `---- 3-pin JST ---- upper stair ---- lower stair
                  5 V
                  PA8 data through 310 ohm
                  GND
```

All grounds are common. Building outputs branch independently from the reinforced
star points; they are not daisy-chained through one another.

## BlackPill and NeoPixel wiring

| Signal | Connection |
|---|---|
| Supply | regulated 5 V |
| MCU | WeAct BlackPill `STM32F401CCU6` |
| NeoPixel data pin | `PA8` |
| Series resistor | 310 ohm used; 270–330 ohm suitable |
| Pixel protocol | GRB, 800 kHz |
| Pixel count | 20 |
| Physical order | pixel 0 highest, pixel 19 lowest |

```text
BlackPill PA8 ---- 310 ohm ---- DIN pixel 0
pixel 0 DOUT ------------------ DIN pixel 1 ---- ... ---- pixel 19
5 V star ---------------------- every pixel 5 V
GND star ---------------------- every pixel GND + BlackPill GND
```

The as-built chain works directly from the STM32's 3.3 V data output. If another
WS2812-compatible batch is unreliable at 5 V supply, add a 5-V AHCT-family level
shifter instead of changing animation timing randomly.

## Stair-module servicing

- LEDs are soldered to flexible leads and mounted in replaceable printed carriers.
- Three-pin header connections allow modules to separate without desoldering the
  entire chain.
- Diffusers unclip from above; a carrier can be pushed upward from below after
  desoldering the affected LED.
- The lowest physical LED has no spacer and is limited to approximately 50% in
  firmware to match the other diffuser brightness.

## As-built power distributor

- one 70 x 90 mm plated perfboard
- one fixed 5 V input
- five fixed 5 V building outputs
- reinforced positive and ground star conductors
- individual thin branch leads only carry the current of their building
- the main input carries the sum of all branches plus controller/stair current

For the photographed five-building build, a regulated **5 V / 3 A** source is sufficient. A
5 V / 5 A source gives useful expansion headroom, but its higher rating does not
force additional current into the load.

If the supply is enlarged substantially, size and fuse the distribution for the
weakest downstream conductor or PCB path rather than for the headline supply
rating. Do not directly parallel independent 5 V power-supply outputs.

## Measured consumption

Measurements were made in series at the 5 V input with all grounds left connected.
The BlackPill remained powered during the individual subtraction tests.

| Configuration / load | Measured current | Approximate power |
|---|---:|---:|
| Complete five-building display + controller + staircase | 1.75 A | 8.75 W |
| Earlier four-building display + controller + staircase | 1.55 A | 7.75 W |
| 20 animated stair NeoPixels | 0.30 A | 1.50 W |
| Tech Tower | 0.50 A | 2.50 W |
| Original other three buildings + BlackPill | 0.75 A | 3.75 W |
| Added Tech Station (incremental) | 0.20 A | 1.00 W |

Round the present installation to **1.8 A** for planning. A voluntary ceiling of
approximately **2.5 A** on the existing 3 A source retains useful margin. Measure
the complete system again after adding each building because current is determined
by its real lighting electronics, not merely by its advertised number of lights.

## Measurement adapter

A reusable inline adapter can measure either the complete district or one building:

```text
supply VBUS ---- multimeter A input
multimeter COM - load VBUS
supply GND ----- load GND directly
```

Use the fused high-current input and DC-current range. The black COM lead is the
outgoing positive path in this series measurement; it is not connected to system
ground. Never place a current-configured multimeter directly across 5 V and GND.

## Bring-up sequence

1. With power disconnected, check resistance between 5 V and GND and inspect all
   USB-C breakout orientations.
2. Power the empty distributor from a current-limited source if available.
3. Verify 5 V and polarity at every output.
4. Install the BlackPill and test the staircase alone.
5. Add buildings one at a time while measuring total current.
6. Confirm that connectors, perfboard conductors and the main input remain cool
   during a sustained full-light test.

