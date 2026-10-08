#!/usr/bin/env python3
"""Regenerate the root SHA-256 manifest for every packaged release file."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SHA256SUMS"
IGNORED_PARTS = {".git", "__pycache__"}


def packaged_files() -> list[Path]:
    files: list[Path] = []
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
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(ROOT).as_posix())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    lines = [
        f"{sha256(path)}  ./{path.relative_to(ROOT).as_posix()}\n"
        for path in packaged_files()
    ]
    MANIFEST.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {len(lines)} entries to {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

