#!/usr/bin/env python3
"""Check availability of CAD tools used by this skill."""

from __future__ import annotations

import importlib.util
import json
import shutil


COMMANDS = ["dwg2dxf", "dwgread", "dwglayers", "ezdxf", "FreeCADCmd", "freecadcmd", "librecad"]
PYTHON_MODULES = ["ezdxf", "shapely", "win32com", "pyautocad"]


def main() -> int:
    result = {
        "commands": {name: shutil.which(name) for name in COMMANDS},
        "python_modules": {
            name: importlib.util.find_spec(name) is not None for name in PYTHON_MODULES
        },
        "notes": [
            "DXF analysis prefers ezdxf.",
            "DWG conversion prefers LibreDWG dwg2dxf when available.",
            "AutoCAD COM paths require local AutoCAD and user approval.",
        ],
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
