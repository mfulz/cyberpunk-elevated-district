# Print models

- `print/stl/` contains the ready-to-slice meshes.
- `print/step/` contains the same print parts as editable BREP geometry.
- `print/parts.csv` is the authoritative parts and quantity list.

All files are already placed in their intended print orientation. Their bounding-box
minimum is at `X=0`, `Y=0`, `Z=0`; no assembly-space coordinates remain in the print
files. Repeated and geometrically identical instances are represented by one file and
their required number is recorded in `parts.csv`.

The largest parts target a 350 x 350 mm build plate. The complete positioned assembly
is intentionally available only as the FreeCAD document under `source/FreeCAD/`.
