# Mechanical assembly

This document gives the recommended build order. The positioned FreeCAD file is
the authoritative reference for orientation and placement:

`models/source/FreeCAD/lumibricks-cyberpunk-mega-structure.FCStd`

Because table construction and chosen screw lengths differ, the release does not
pretend there is one universal fastener schedule. Use the shortest M3 screw that
fully engages its insert without bottoming out.

## 1. Inventory and dry fit

1. Verify every quantity against `models/print/parts.csv`.
2. Deburr cable passages, insert pockets and mating edges without enlarging them
   unnecessarily.
3. Dry-fit both stair modules, all deck/platform joints and every truss assembly.
4. Keep the table-anchor frame separate until its real mounting position has
   been checked against the furniture.

Do not compensate a printer-wide dimensional error by heavily filing every
individual joint. Correct the print process before producing the remaining large
parts.

## 2. Build the trusses

Each truss is assembled from two outer shells and one contrasting inlay.

- lower level: three rear shells, three front shells and three inlays
- upper level, long: four identical shells and two inlays
- upper level, short: four identical shells and two inlays

Recommended process:

1. Dry-clamp each shell/inlay/shell sandwich on a flat surface.
2. Confirm that both end interfaces remain square and that no adhesive enters
   screw passages.
3. Bond the laminate with ABS-compatible CA or solvent cement.
4. Keep it clamped until the adhesive has developed handling strength.
5. Recheck the end faces before installing it in the structure.

The truss laminate is not decorative filler: both faces and the inlay cooperate
to prevent bending and buckling.

## 3. Install heat-set inserts

The CAD contains up to 86 insert pockets, including redundant/optional mounting
positions.

1. Use inserts around 4.6 mm outside diameter and 5–6 mm length with the modelled
   4.5 mm pockets.
2. Insert them squarely with a temperature-controlled tip.
3. Stop flush with, or slightly below, the bearing surface.
4. Let the plastic cool before running a screw into the insert.
5. Use a mating part or loose screw to verify alignment before final assembly.

Do not install every optional insert merely because a pocket exists. Populate the
positions used by the chosen assembly and keep the remaining pockets as future
mounting options.

## 4. Assemble and test the lighting modules

Complete the lighting before the staircases become difficult to access.

1. Solder the 20 NeoPixels as one continuous chain from the highest step to the
   lowest step.
2. Route `5V`, `GND` and data through the provided downward passages.
3. Use the separable three-contact module connection between staircase sections.
4. Fit the printed carriers and spacers.
5. Fit the upper-stair correction carriers to the five upper openings.
6. Power the chain at low brightness and verify colour order, data direction and
   every pixel.
7. Clip in the diffusers only after the electrical test succeeds.

The standard diffusers are removable from above. A failed LED can therefore be
desoldered from below, pushed upward and replaced without reprinting a complete
staircase.

## 5. Assemble the lower structure

1. Join the four lower deck plates in their FreeCAD reference positions.
2. Install the three lower trusses between their corresponding mounts.
3. Attach the main staircase module at the designed deck interfaces.
4. Leave screws slightly loose until all lower interfaces are engaged.
5. Square the assembly, then tighten progressively rather than fully tightening
   one corner first.

At this stage the partial structure may still flex. Final stiffness appears only
after the stair modules, upper trusses and both upper platforms close the spatial
frame.

## 6. Add the upper structure

1. Attach the five-step upper stair module to the main stair assembly.
2. Install both long and both short upper trusses in the positions shown in the
   FreeCAD assembly.
3. Place the large and small upper platforms on the truss interfaces.
4. Start every platform screw before tightening any one interface fully.
5. Confirm that platform edges meet without forced twist.
6. Tighten the stair/platform joints, then the truss ends, while checking the
   structure for square.

With both platforms installed, the decks act as large shear panels and the stair
modules couple the levels. The resulting spatial frame is substantially stiffer
than any isolated component.

## 7. Mount to the table

The supplied anchor frame was designed for the original table and deliberately
extends beyond its edge. Furniture construction varies too much for a universal
screw recommendation.

1. Inspect the tabletop for hollow sections, internal rails and inaccessible
   cavities.
2. Position the complete empty structure and verify bed/chair/walkway clearance.
3. Mark and drill only after confirming the final overhang.
4. Fix the anchor frame laterally and from above where the real table permits.
5. Attach the staircase and lower frame to the already secured anchor.
6. Load the platforms gradually before placing the full buildings.

Do not use the photographed manual load test as an engineering load rating. The
release is a display structure, not furniture or a human-supporting platform.

## 8. Electronics enclosure and buildings

1. Mount the populated 70 x 90 mm perfboard on the enclosure standoffs.
2. Verify that the lid opens without pulling on the staircase cable.
3. Attach the enclosure beneath the lower structure in its CAD position.
4. Route each building lead independently back to the star distributor.
5. Use the exposed trusses as deliberate cable-routing features while protecting
   leads from snagging.
6. Place buildings only after a final polarity and short-circuit check.

The platforms intentionally remain rearrangeable. Use removable pads if a
building needs slip resistance; avoid permanently bonding commercial sets to the
printed structure.

