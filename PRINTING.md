# Printing guide

The supplied files are already moved out of assembly space and placed in their
intended print orientation. `models/print/parts.csv` is authoritative for
quantity, orientation and bounding-box dimensions.

## Printer requirements

- build area: at least **350 x 350 mm**
- usable Z height: at least **200 mm**
- enclosed and heat-soaked machine strongly recommended for ABS/ASA
- reliable long-print operation; the largest parts occupy most of the bed

Do not scale individual parts independently. Their interfaces, insert pockets
and platform alignment depend on common dimensions.

## As-built reference profile

These settings document the successful build. They are not universal filament
presets:

| Parameter | As-built reference |
|---|---:|
| Layer height | 0.20 mm |
| Perimeters | 4 |
| Solid top layers | 5 |
| Solid bottom layers | 5 |
| Main staircase infill | 18% |
| Upper structural truss infill | 55% |
| Table-anchor infill | 10% |
| Diffuser infill | 100% |
| Bed temperature for ABS | 110 degrees C |
| Chamber before starting large ABS prints | at least 50 degrees C |

The original high-speed ABS was run as hot as 285 degrees C after material-specific
testing. Do **not** transfer that temperature blindly to another ABS/ASA, especially
transparent material. The transparent diffuser material showed optical degradation
at temperatures that were harmless to the opaque structural filament.

The original printer used a high-flow hotend and reached approximately 240–260
mm/s on suitable paths. That speed is not a release requirement. Set a tested
volumetric-flow limit, retain conservative outer-wall acceleration and let the
slicer reduce speed where geometry or surface quality requires it.

## Part-specific notes

### Platforms and lower deck plates

- Use the supplied orientation; integrated mounts face upward while printing.
- These large flat parts are the most sensitive to chamber and bed temperature
  gradients.
- Let them cool in the closed chamber until they release naturally whenever
  practical. Removing them hot strongly increases corner lift.

### Staircase modules

- Print the bases in the supplied orientation.
- The 15-step module was successfully printed at 18% infill with four perimeters.
- Verify all LED and cable passages in the slicer before committing to the long
  print.

### Trusses

- Each visible truss is a laminate: two outer shell pieces and one coloured
  inlay.
- Upper long and short shell geometries are symmetric/deduplicated; their CSV
  quantities already include both faces.
- The successful upper trusses used 55% infill. Treat this as a conservative
  structural reference, not a claim that every truss requires that exact value.
  The thin shell geometry and layer bonding matter more than chasing a nominal
  100% value.

### NeoPixel carriers and diffusers

- Print all diffusers at 100% infill; the internal toolpath provides the useful
  light scattering and hides the individual LED spot.
- Keep carrier dimensions unchanged. Their snap fit and LED distance control
  the visual result.
- There are only 14 standard spacers for 15 main-stair pixels. The lowest pixel
  intentionally sits directly below its diffuser and is limited to 50% in the
  supplied firmware.
- The five upper-stair parts are correction adapters because the corresponding
  large recess was omitted from the finished upper-stair body.

### Electronics enclosure

- The enclosure matches the as-built 70 x 90 mm perfboard and the selected
  USB-C breakout boards.
- Breakout-board dimensions are not standardized. Compare your boards with the
  STEP model before printing the enclosure.

## Dimensional strategy

The original Voron was calibrated closely enough for approximately 0.2 mm
assembly clearances and 4.5 mm heat-set-insert pockets. Another printer/material
combination can differ through extrusion width, flow multiplier, shrinkage and
first-layer deformation.

Before printing multi-hour parts:

1. Print a representative insert pocket and mating tongue/groove.
2. Confirm that the selected M3 inserts seat without splitting the part.
3. Check first-layer elephant-foot compensation.
4. Apply global material shrink compensation only from measured calibration
   parts; do not alter isolated release parts by eye.

## Cooling large ABS/ASA parts

The build benefited substantially from a slow, controlled cooldown. The useful
goal is not merely a low final temperature but avoiding a sudden increase in
cooling rate while the part can still move. Keep the chamber closed, retain
circulation if it produces a uniform chamber, and avoid pulling a large plate
from a hot bed directly into room air.
