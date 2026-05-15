#!/usr/bin/env python3
"""Report available tools for construction design and concept workflows."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
import sys
from typing import Any


MODULES = {
    "numpy": "Numeric calculations for parametric options",
    "pandas": "Option tables and design decision matrices",
    "shapely": "Planar geometry, buffers, site footprints",
    "geopandas": "GIS/site analysis with spatial dataframes",
    "osmnx": "OpenStreetMap street/building/context analysis",
    "networkx": "Circulation and adjacency graph analysis",
    "matplotlib": "Quick charts and site diagrams",
    "ifcopenshell": "IFC model read/write and Bonsai ecosystem",
    "ladybug": "Climate and solar design helpers",
    "honeybee": "Daylight and energy design model helpers",
    "honeybee_energy": "Energy model preparation",
    "openstudio": "OpenStudio/EnergyPlus workflows",
    "compas": "Computational design framework",
    "topologicpy": "Spatial topology and building intelligence",
    "specklepy": "AEC data exchange with Speckle",
    "trimesh": "Mesh geometry checks and conversions",
}

COMMANDS = {
    "FreeCADCmd": "FreeCAD command line for parametric CAD/BIM scripts",
    "freecadcmd": "FreeCAD command line alternative name",
    "blender": "Blender/Bonsai visual concept and render",
    "qgis": "QGIS desktop GIS",
    "qgis_process": "QGIS processing command line",
    "energyplus": "EnergyPlus simulation engine",
    "openstudio": "OpenStudio CLI",
    "python": "Python runtime",
    "pip": "Python package installer",
    "node": "Node runtime for web viewers or tooling",
}


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def command_path(name: str) -> str | None:
    return shutil.which(name)


def build_report() -> dict[str, Any]:
    return {
        "runtime": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "modules": [
            {"name": name, "available": module_available(name), "purpose": purpose}
            for name, purpose in MODULES.items()
        ],
        "commands": [
            {
                "name": name,
                "available": command_path(name) is not None,
                "path": command_path(name),
                "purpose": purpose,
            }
            for name, purpose in COMMANDS.items()
        ],
    }


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# İnşaat Tasarım Araç Durumu",
        "",
        f"- Python: {report['runtime']['python']}",
        f"- Platform: {report['runtime']['platform']}",
        "",
        "## Python Modülleri",
        "",
        "| Modül | Durum | Amaç |",
        "|---|---|---|",
    ]
    for item in report["modules"]:
        status = "var" if item["available"] else "eksik"
        lines.append(f"| `{item['name']}` | {status} | {item['purpose']} |")
    lines.extend(["", "## Komutlar", "", "| Komut | Durum | Yol | Amaç |", "|---|---|---|---|"])
    for item in report["commands"]:
        status = "var" if item["available"] else "eksik"
        path = item["path"] or "-"
        lines.append(f"| `{item['name']}` | {status} | `{path}` | {item['purpose']} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()
    report = build_report()
    print(to_markdown(report) if args.format == "markdown" else json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
