#!/usr/bin/env python3
"""Create a safe DWG to DXF conversion plan without mutating files."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dwg", help="DWG file")
    parser.add_argument("--output-dir", default=None, help="Output directory for converted DXF")
    args = parser.parse_args()

    source = Path(args.dwg)
    output_dir = Path(args.output_dir) if args.output_dir else source.parent / "cad-output"
    target = output_dir / f"{source.stem}.dxf"
    dwg2dxf = shutil.which("dwg2dxf")
    freecad = shutil.which("FreeCADCmd") or shutil.which("freecadcmd")
    librecad = shutil.which("librecad")

    commands: list[str] = []
    if dwg2dxf:
        commands.append(f'"{dwg2dxf}" "{source}"')
    if freecad:
        commands.append(f'"{freecad}" # use FreeCAD import/export macro after user review')
    if librecad:
        commands.append(f'"{librecad}" "{source}" # GUI QA / export as DXF')

    result = {
        "source": str(source.resolve()),
        "output_dir": str(output_dir.resolve()),
        "target_dxf": str(target.resolve()),
        "available_tools": {
            "dwg2dxf": dwg2dxf,
            "freecadcmd": freecad,
            "librecad": librecad,
        },
        "recommended_route": "dwg2dxf_then_ezdxf_qa" if dwg2dxf else "install_libredwg_or_use_freecad_librecad",
        "commands_to_review": commands,
        "qa_after_conversion": [
            "Open produced DXF with ezdxf.",
            "Run DXF audit.",
            "Compare layer/block/entity counts with expected drawing scope.",
            "Check units, scale, xrefs, proxy entities, hatches, and paperspace.",
            "Use visual QA in LibreCAD/FreeCAD/AutoCAD when available.",
        ],
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
