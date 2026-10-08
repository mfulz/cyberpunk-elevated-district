#!/usr/bin/env python3
"""Verify release completeness, hashes, print sets and packaged firmware."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import struct
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SHA256SUMS"
IGNORED_PARTS = {".git", "__pycache__"}

REQUIRED_DOCS = {
    "README.md",
    "ASSEMBLY.md",
    "PRINTING.md",
    "ELECTRONICS.md",
    "BOM.md",
    "BOM.csv",
    "LICENSE.md",
    "LICENSES/CC-BY-NC-SA-4.0.txt",
    "LICENSES/MIT.txt",
    "models/README.md",
    "models/print/parts.csv",
    "models/source/FreeCAD/lumibricks-cyberpunk-mega-structure.FCStd",
    "images/README.md",
    "images/final/hero-night.jpg",
    "images/video/stair-animation.mp4",
}


class VerificationError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def packaged_files() -> set[str]:
    result: set[str] = set()
    for path in ROOT.rglob("*"):
        if not path.is_file() or path == MANIFEST:
            continue
        relative = path.relative_to(ROOT)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        if relative.parts[:3] == ("firmware", "neopixel-stair-20", "build"):
            continue
        if path.suffix in {".pyc", ".tmp", ".bak", ".FCStd1"}:
            continue
        result.add(relative.as_posix())
    return result


def verify_required_files() -> None:
    missing = sorted(path for path in REQUIRED_DOCS if not (ROOT / path).is_file())
    if missing:
        raise VerificationError(f"Missing required files: {', '.join(missing)}")


def verify_local_document_links() -> None:
    markdown_link = re.compile(r"\[[^]]*\]\(([^)]+)\)")
    html_source = re.compile(r'<(?:img|source)[^>]+src="([^"]+)"')
    checked = 0

    for document in ROOT.rglob("*.md"):
        text = document.read_text(encoding="utf-8")
        targets = markdown_link.findall(text) + html_source.findall(text)
        for raw_target in targets:
            target = raw_target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            path = (document.parent / target).resolve()
            try:
                path.relative_to(ROOT.resolve())
            except ValueError as exc:
                raise VerificationError(
                    f"Document link escapes release root: {document.relative_to(ROOT)} -> {raw_target}"
                ) from exc
            if not path.exists():
                raise VerificationError(
                    f"Broken local link: {document.relative_to(ROOT)} -> {raw_target}"
                )
            checked += 1

    print(f"OK: {checked} local documentation links")


def verify_publication_media() -> None:
    image_root = ROOT / "images"
    images = sorted(
        path for path in image_root.rglob("*") if path.suffix.lower() in {".jpg", ".png"}
    )
    if len(images) != 23:
        raise VerificationError(f"Expected 23 publication images, found {len(images)}")

    for path in images:
        data = path.read_bytes()
        if path.suffix.lower() == ".jpg":
            if not data.startswith(b"\xff\xd8") or not data.endswith(b"\xff\xd9"):
                raise VerificationError(f"Invalid JPEG: {path.relative_to(ROOT)}")
        elif not data.startswith(b"\x89PNG\r\n\x1a\n"):
            raise VerificationError(f"Invalid PNG: {path.relative_to(ROOT)}")

    video = image_root / "video/stair-animation.mp4"
    completed = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=codec_type,codec_name,width,height:format=duration",
            "-of",
            "json",
            str(video),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode:
        raise VerificationError(f"Invalid publication video: {completed.stdout.strip()}")
    metadata = json.loads(completed.stdout)
    streams = metadata.get("streams", [])
    video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
    if len(video_streams) != 1 or video_streams[0].get("codec_name") != "h264":
        raise VerificationError("Publication video must contain exactly one H.264 video stream")
    if audio_streams:
        raise VerificationError("Publication video must be muted")

    print(f"OK: {len(images)} publication images and muted H.264 video")


def verify_manifest() -> None:
    if not MANIFEST.is_file():
        raise VerificationError("Missing SHA256SUMS")

    recorded: dict[str, str] = {}
    for number, raw in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if not raw:
            continue
        try:
            expected, name = raw.split("  ", 1)
        except ValueError as exc:
            raise VerificationError(f"Malformed SHA256SUMS line {number}") from exc
        if len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
            raise VerificationError(f"Invalid digest on SHA256SUMS line {number}")
        normalized = name.removeprefix("./")
        if normalized in recorded:
            raise VerificationError(f"Duplicate manifest entry: {normalized}")
        recorded[normalized] = expected

    actual = packaged_files()
    listed = set(recorded)
    missing = sorted(actual - listed)
    stale = sorted(listed - actual)
    if missing or stale:
        details = []
        if missing:
            details.append("unhashed files: " + ", ".join(missing))
        if stale:
            details.append("missing files still in manifest: " + ", ".join(stale))
        raise VerificationError("; ".join(details))

    for relative, expected in sorted(recorded.items()):
        actual_digest = sha256(ROOT / relative)
        if actual_digest != expected:
            raise VerificationError(f"Checksum mismatch: {relative}")

    print(f"OK: {len(recorded)} root checksums")


def verify_binary_stl(path: Path) -> None:
    data = path.read_bytes()
    if len(data) < 84:
        raise VerificationError(f"STL too small: {path.relative_to(ROOT)}")
    triangle_count = struct.unpack_from("<I", data, 80)[0]
    if triangle_count == 0 or len(data) != 84 + 50 * triangle_count:
        raise VerificationError(f"Invalid binary STL: {path.relative_to(ROOT)}")


def verify_print_models() -> None:
    csv_path = ROOT / "models/print/parts.csv"
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 23:
        raise VerificationError(f"Expected 23 unique print parts, found {len(rows)}")

    names: set[str] = set()
    for row in rows:
        name = row["part"]
        if not name or name in names:
            raise VerificationError(f"Missing or duplicate print-part name: {name!r}")
        names.add(name)
        if int(row["quantity"]) <= 0:
            raise VerificationError(f"Invalid quantity for {name}")
        dimensions = [float(row[key]) for key in ("size_x_mm", "size_y_mm", "size_z_mm")]
        if any(value <= 0 for value in dimensions):
            raise VerificationError(f"Invalid dimensions for {name}")
        if dimensions[0] > 350.001 or dimensions[1] > 350.001:
            raise VerificationError(f"Part exceeds documented 350 x 350 mm bed: {name}")

        step = ROOT / "models/print/step" / f"{name}.step"
        stl = ROOT / "models/print/stl" / f"{name}.stl"
        if not step.is_file() or not stl.is_file():
            raise VerificationError(f"Missing STEP/STL pair for {name}")
        step_head = step.read_bytes()[:256]
        if b"ISO-10303-21" not in step_head:
            raise VerificationError(f"Invalid STEP header: {step.relative_to(ROOT)}")
        verify_binary_stl(stl)

    step_names = {path.stem for path in (ROOT / "models/print/step").glob("*.step")}
    stl_names = {path.stem for path in (ROOT / "models/print/stl").glob("*.stl")}
    if step_names != names or stl_names != names:
        raise VerificationError("Print directories and parts.csv do not contain identical sets")

    print(f"OK: {len(rows)} STEP/STL print-part pairs")


def verify_nested_manifests() -> None:
    checks = [
        (ROOT / "models/source/SHA256SUMS", ROOT),
        (
            ROOT / "firmware/neopixel-stair-20/SHA256SUMS",
            ROOT / "firmware/neopixel-stair-20",
        ),
    ]
    for manifest, working_directory in checks:
        completed = subprocess.run(
            ["sha256sum", "-c", str(manifest)],
            cwd=working_directory,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if completed.returncode:
            raise VerificationError(completed.stdout.strip())
    print("OK: nested source and firmware checksums")


def verify_firmware() -> None:
    script = ROOT / "firmware/neopixel-stair-20/verify_release.py"
    completed = subprocess.run(
        [sys.executable, str(script)],
        cwd=script.parent,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode:
        raise VerificationError(completed.stdout.strip())
    print("OK: packaged BIN/UF2 firmware payload")


def main() -> int:
    try:
        verify_required_files()
        verify_local_document_links()
        verify_publication_media()
        verify_manifest()
        verify_print_models()
        verify_nested_manifests()
        verify_firmware()
    except (OSError, ValueError, VerificationError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    print("Release verification complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
