#!/usr/bin/env python3
"""Export deduplicated, print-oriented STEP/STL files from the release assembly.

Run with FreeCADCmd from the repository root:

    FreeCADCmd tools/export_print_models.py

The assembly document itself is never modified.  Every exported shape is copied,
oriented for printing, and translated so its bounding-box minimum is at 0/0/0.
"""

from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path

import FreeCAD as App
import MeshPart
import Part


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "models/source/FreeCAD/lumibricks-cyberpunk-mega-structure.FCStd"
PRINT_DIR = ROOT / "models/print"
STEP_DIR = PRINT_DIR / "step"
STL_DIR = PRINT_DIR / "stl"


# filename, FreeCAD object name, quantity, orientation, note
PARTS = [
    ("upper-platform-large", "Body037", 1, "flip-x", "Print upside down; integrated mounts point upward."),
    ("upper-platform-small", "Body038", 1, "flip-x", "Print upside down; integrated mounts point upward."),
    ("table-anchor-frame", "Body043", 1, "flip-x", "Large flat face on build plate."),
    ("main-staircase-15-step", "Fusion009", 1, "as-designed", "Base on build plate."),
    ("lower-deck-plate-01", "Body044", 1, "flip-x", "Print upside down; integrated mounts point upward."),
    ("lower-deck-plate-02", "Body045", 1, "flip-x", "Print upside down; integrated mounts point upward."),
    ("lower-deck-plate-03", "Body046", 1, "flip-x", "Print upside down; integrated mounts point upward."),
    ("lower-deck-plate-04", "Body047", 1, "flip-x", "Print upside down; integrated mounts point upward."),
    ("lower-truss-rear-shell", "Pocket193", 3, "largest-face", "One unique model; print three copies."),
    ("lower-truss-front-shell", "Pocket194", 3, "largest-face", "One unique model; print three copies."),
    ("lower-truss-inlay", "U01_INLAY015", 3, "largest-face", "One unique model; print three copies."),
    ("upper-truss-long-shell", "A01_DRUCKSCHALE_HINTEN004", 4, "largest-face", "Rear/front geometry is identical; print four copies."),
    ("upper-truss-long-inlay", "A01_INLAY004", 2, "largest-face", "One unique model; print two copies."),
    ("upper-truss-short-shell", "A03_DRUCKSCHALE_HINTEN004", 4, "largest-face", "Rear/front geometry is identical; print four copies."),
    ("upper-truss-short-inlay", "A03_INLAY004", 2, "largest-face", "One unique model; print two copies."),
    ("neopixel-standard-carrier", "Body049", 15, "as-designed", "For the 15-step main staircase."),
    ("neopixel-standard-diffuser", "Body050", 15, "as-designed", "Transparent material; for the 15-step main staircase."),
    ("neopixel-standard-spacer", "Body051", 14, "as-designed", "One main-stair LED is installed without a spacer."),
    ("upper-staircase-5-step", "Body059", 1, "as-designed", "Base on build plate."),
    ("electronics-enclosure-base", "Body062", 1, "as-designed", "Bottom on build plate."),
    ("electronics-enclosure-lid", "Body063", 1, "flip-x", "Outer top surface on build plate."),
]


# These two adapters were created after the upper staircase recess was omitted.
# They are final print parts but are not separate placed instances in the flattened
# assembly document.
EXTERNAL_PARTS = [
    (
        "upper-stair-neopixel-carrier-adapter",
        ROOT / "models/source/STEP/upper-stair-neopixel-carrier-adapter-source.step",
        5,
        "as-designed",
        "Correction carrier for the five upper-stair LEDs.",
    ),
    (
        "upper-stair-neopixel-diffuser",
        ROOT / "models/source/STEP/upper-stair-neopixel-diffuser-source.step",
        5,
        "as-designed",
        "Correction diffuser for the five upper-stair LEDs.",
    ),
]


def translate_to_origin(shape: Part.Shape) -> Part.Shape:
    result = shape.copy()
    box = result.BoundBox
    result.translate(App.Vector(-box.XMin, -box.YMin, -box.ZMin))
    return result


def orient(shape: Part.Shape, mode: str) -> Part.Shape:
    result = shape.copy()

    if mode == "flip-x":
        result.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), 180)
    elif mode == "largest-face":
        planar = [face for face in result.Faces if face.Surface.TypeId == "Part::GeomPlane"]
        if not planar:
            raise RuntimeError("No planar face available for print orientation")
        face = max(planar, key=lambda item: item.Area)
        u0, u1, v0, v1 = face.ParameterRange
        normal = face.normalAt((u0 + u1) / 2, (v0 + v1) / 2)
        normal.normalize()
        rotation = App.Rotation(normal, App.Vector(0, 0, -1))
        result.Placement = App.Placement(App.Vector(), rotation).multiply(result.Placement)
    elif mode != "as-designed":
        raise ValueError(f"Unknown orientation mode: {mode}")

    return translate_to_origin(result)


def export_shape(shape: Part.Shape, stem: str) -> tuple[Path, Path]:
    temp = App.newDocument("PrintExport")
    obj = temp.addObject("Part::Feature", "PrintPart")
    obj.Label = stem
    obj.Shape = shape

    step_path = STEP_DIR / f"{stem}.step"
    stl_path = STL_DIR / f"{stem}.stl"
    Part.export([obj], str(step_path))
    mesh = MeshPart.meshFromShape(
        Shape=shape,
        LinearDeflection=0.05,
        AngularDeflection=math.radians(20),
        Relative=False,
    )
    mesh.write(str(stl_path))
    App.closeDocument(temp.Name)
    return step_path, stl_path


def main() -> None:
    global PRINT_DIR, STEP_DIR, STL_DIR

    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)

    staging = PRINT_DIR.with_name(".print-staging")
    if staging.exists():
        shutil.rmtree(staging)
    (staging / "step").mkdir(parents=True)
    (staging / "stl").mkdir(parents=True)

    old_print_dir, old_step_dir, old_stl_dir = PRINT_DIR, STEP_DIR, STL_DIR
    PRINT_DIR, STEP_DIR, STL_DIR = staging, staging / "step", staging / "stl"

    document = App.openDocument(str(SOURCE))
    rows = []
    try:
        for stem, object_name, quantity, mode, note in PARTS:
            obj = document.getObject(object_name)
            if obj is None or not hasattr(obj, "Shape") or obj.Shape.isNull():
                raise RuntimeError(f"Missing or empty object: {object_name}")
            shape = orient(obj.Shape, mode)
            step_path, stl_path = export_shape(shape, stem)
            box = shape.BoundBox
            rows.append(
                [stem, quantity, obj.Label, mode, f"{box.XLength:.3f}", f"{box.YLength:.3f}", f"{box.ZLength:.3f}", note]
            )

        for stem, source_path, quantity, mode, note in EXTERNAL_PARTS:
            if not source_path.is_file():
                raise FileNotFoundError(source_path)
            shape = orient(Part.read(str(source_path)), mode)
            export_shape(shape, stem)
            box = shape.BoundBox
            rows.append(
                [stem, quantity, "Upper-stair light correction", mode, f"{box.XLength:.3f}", f"{box.YLength:.3f}", f"{box.ZLength:.3f}", note]
            )
    finally:
        App.closeDocument(document.Name)

    with (staging / "parts.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["part", "quantity", "assembly_label", "print_orientation", "size_x_mm", "size_y_mm", "size_z_mm", "note"])
        writer.writerows(rows)

    # Replace the old assembly-space exports only after every new export succeeded.
    PRINT_DIR, STEP_DIR, STL_DIR = old_print_dir, old_step_dir, old_stl_dir
    if PRINT_DIR.exists():
        shutil.rmtree(PRINT_DIR)
    staging.rename(PRINT_DIR)
    print(f"Exported {len(rows)} unique print parts to {PRINT_DIR}")


# This file is an executable FreeCADCmd script, not an importable library.
main()
