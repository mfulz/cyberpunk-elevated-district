# Bill of materials / Einkaufsliste

This list covers the elevated structure, the 20-step NeoPixel lighting and the
as-built power-distribution box. Lumibricks buildings, the supporting table and
the 3D printer are not included.

The printable part quantities are maintained separately in
[`models/print/parts.csv`](models/print/parts.csv).

## Electronics

| Required | Sensible purchase quantity | Component | Relevant specification |
|---:|---:|---|---|
| 1 | 1 | WeAct BlackPill | `STM32F401CCU6`, USB-C version; TinyUF2-compatible |
| 20 | 25 | Individual NeoPixel modules | WS2812B-compatible, 5 V, GRB/800 kHz, small round breakout PCB with `5V`, `GND`, `DIN`, `DOUT` pads |
| 1 | assortment | Series resistor | 310 ohm used in the build; 270–330 ohm is suitable between `PA8` and first `DIN` |
| 1 | 1–2 | Perfboard | 70 x 90 mm, 2.54 mm pitch, plated through-holes |
| 6 | 7–10 | USB-C receptacle breakouts | Power-only breakout matching the enclosure openings; used as one input and five outputs |
| up to 5 | 10 | USB-C male solder breakouts | Power-only, preferably four large solder pads; for the visible custom building leads |
| 1 pair | 5 pairs | 3-pin JST set | JST-XH-style plug/socket for `5V`, data and ground between controller box and staircase |
| 2 x 20 contacts | 2 strips | 2.54 mm socket headers | Removable mounting of the BlackPill on the perfboard |
| about 4 connections | 1 strip each | 2.54 mm male and female breakaway headers | Three contacts per separable staircase-module connection |

Buy spare NeoPixels. They cost almost nothing compared with reopening an assembled
staircase, and the design intentionally allows individual replacement.

## Wiring and power

| Quantity | Item | Use |
|---:|---|---|
| 1–2 m each | red, black and yellow flexible wire, 26 AWG | NeoPixel chain and visible building leads |
| about 0.5 m each | red and black flexible wire, 20–22 AWG | Internal 5 V/GND star distribution on the perfboard |
| as needed | heat-shrink tubing | Insulation and strain relief on custom leads |
| 1 | regulated 5 V supply | 5 V / 3 A is verified for the photographed 1.75 A build; 5 V / 5 A is a practical expansion target |
| 1 | matching power cable | Must deliver plain 5 V to the controller-box input |

### USB-C limitation of the as-built distributor

The six connectors are used as a **fixed 5 V power bus**, not as standards-compliant
USB-C/USB-PD ports. The simple breakouts do not negotiate voltage or power.

- Feed the box with 5 V only.
- Do not connect laptops, phones or arbitrary USB-C equipment.
- A charger advertised as “60 W” commonly provides only 5 V / 3 A without PD
  negotiation; the 60 W label does not mean 60 W are available to this circuit.
- If a USB-C-to-USB-C source is used, the input breakout must provide correct CC
  resistors. A known 5 V USB-A-to-C supply path avoids that ambiguity.

The complete five-building display, 20 NeoPixels and BlackPill measured about
1.75 A at 5 V. Treat this as one as-built reference rather than a specification
for other buildings; measure the total again after each expansion.

## Mechanical hardware

| Required / modelled | Buy | Component | Notes |
|---:|---:|---|---|
| up to 86 | 100 | M3 heat-set inserts | CAD pockets are 4.5 mm diameter; inserts around 4.6 mm OD and 5–6 mm length fit the intended process |
| project-dependent | 150–200 assorted | M3 socket-head screws | Useful range: M3 x 8, 10, 12, 16, 20, 25 and 30 mm |
| optional | 100 | M3 washers | Useful during final alignment and where screw heads bear directly on plastic |
| table-dependent | as required | Table/furniture mounting screws | Select for the actual tabletop construction; these cannot be specified universally |

The CAD intentionally contains redundant/optional insert positions. Therefore the
modelled maximum of 86 inserts is more useful than pretending there is one exact screw
count for every installation.

## Adhesives and assembly consumables

- medium-viscosity CA glue suitable for ABS/ASA, or ABS solvent cement
- a small amount of removable adhesive for LED carriers where desired
- solder and flux
- heat-set-insert tip or temperature-controlled soldering iron

The truss shells and coloured inlays are separate print parts and are bonded after
printing. Structural attachment to platforms and stair modules is handled by M3 screws
and heat-set inserts.

## Filament planning

The colour scheme of the photographed build is:

| Suggested stock | Material/colour | Parts |
|---:|---|---|
| 4 x 1 kg | ABS/ASA, midnight blue or similarly dark blue | both staircase modules, table anchor frame, truss inlays, electronics enclosure and LED carriers/spacers |
| 3 x 1 kg | ABS/ASA, medium grey | platforms, lower deck plates and outer truss shells |
| at least 250 g | natural/transparent material | 20 diffusers, printed at 100% infill in the original build |

The dark-blue and grey quantities are deliberately purchase-planning values with
reserve, **not slicer-derived exact consumption figures**. Actual usage changes heavily
with perimeter count, top/bottom layers and infill. Slice the supplied STLs with the
intended profile before ordering an exact minimum.

## Not included

- Lumibricks buildings and their original lighting electronics
- supporting desk/table
- mains-side wiring
- USB-C PD trigger or protocol electronics
- tools and 3D printer
