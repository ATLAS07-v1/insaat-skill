#!/usr/bin/env python3
"""Inventory construction input files and recommend processing tools.

Usage:
  python inspect_construction_inputs.py <file-or-folder> [<file-or-folder> ...]

This script uses only the Python standard library. It does not open archives,
execute macros, or parse document content.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable


CATEGORY_TO_TOOLS = {
    "document": ["markitdown", "docling", "pymupdf", "pdfplumber"],
    "spreadsheet": ["pandas", "openpyxl"],
    "cad_dxf": ["ezdxf", "freecad"],
    "cad_dwg": ["libredwg", "freecad", "cad-autocad-dwg-dxf-isleme"],
    "bim_ifc": ["ifcopenshell", "freecad"],
    "image": ["opencv", "docling"],
    "archive": ["inventory_only"],
    "text_data": ["python_stdlib", "pandas"],
    "unknown": ["manual_review"],
}

EXTENSION_CATEGORY = {
    ".pdf": "document",
    ".doc": "document",
    ".docx": "document",
    ".ppt": "document",
    ".pptx": "document",
    ".xls": "spreadsheet",
    ".xlsx": "spreadsheet",
    ".xlsm": "spreadsheet",
    ".csv": "text_data",
    ".tsv": "text_data",
    ".json": "text_data",
    ".xml": "text_data",
    ".md": "text_data",
    ".txt": "text_data",
    ".yaml": "text_data",
    ".yml": "text_data",
    ".dxf": "cad_dxf",
    ".dwg": "cad_dwg",
    ".ifc": "bim_ifc",
    ".ifczip": "bim_ifc",
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".tif": "image",
    ".tiff": "image",
    ".webp": "image",
    ".zip": "archive",
    ".7z": "archive",
    ".rar": "archive",
}


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_files(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_file():
            yield path
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file():
                    yield child


def classify(path: Path) -> str:
    return EXTENSION_CATEGORY.get(path.suffix.lower(), "unknown")


def risk_flags(path: Path, category: str) -> list[str]:
    flags: list[str] = []
    suffix = path.suffix.lower()
    name = path.name.lower()
    if category == "archive":
        flags.append("archive_inventory_only")
    if suffix in {".xlsm", ".docm", ".pptm"}:
        flags.append("macro_possible")
    if suffix in {".exe", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".py"}:
        flags.append("executable_do_not_run")
    if "password" in name or "parola" in name or "secret" in name:
        flags.append("sensitive_name_check")
    if category == "cad_dwg":
        flags.append("dwg_conversion_requires_qa")
    return flags


def inspect(path: Path) -> dict:
    category = classify(path)
    return {
        "path": str(path.resolve()),
        "name": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "category": category,
        "recommended_tools": CATEGORY_TO_TOOLS[category],
        "risk_flags": risk_flags(path, category),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Input files or folders")
    args = parser.parse_args()

    roots = [Path(item) for item in args.paths]
    files = [inspect(path) for path in iter_files(roots)]
    result = {
        "roots": [str(path.resolve()) for path in roots],
        "file_count": len(files),
        "files": files,
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
