#!/usr/bin/env python3
"""Report available tools for bid, BOQ, and construction cost workflows."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
import sys
from typing import Any


MODULES = {
    "pandas": "CSV/XLSX cost tables, grouping, pivots, QA checks",
    "openpyxl": "Read/write existing XLSX templates",
    "xlsxwriter": "Create formatted XLSX bid reports",
    "odfdo": "OpenDocument ODS/ODT generation and parsing",
    "odf": "ODF support via odfpy",
    "numpy": "Numeric checks and tolerances",
    "pypdf": "PDF offer/takeoff text extraction fallback",
    "pdfplumber": "PDF text/table extraction",
    "camelot": "PDF table extraction",
    "rapidfuzz": "Fuzzy match between supplier descriptions and BOQ items",
    "babel": "Currency/locale formatting",
    "ifcopenshell": "IFC quantity and cost item integration",
    "ifc5d": "IfcOpenShell 5D cost utilities",
    "yaml": "YAML config and agent metadata",
}

COMMANDS = {
    "python": "Python runtime",
    "pip": "Python package installer",
    "soffice": "LibreOffice CLI for XLSX/ODS/PDF conversion",
    "libreoffice": "LibreOffice CLI alternative",
    "qpdf": "PDF repair and inspection",
    "ifc5d": "IfcOpenShell 5D command line if installed",
}


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def command_path(name: str) -> str | None:
    return shutil.which(name)


def build_report() -> dict[str, Any]:
    return {
        "runtime": {"python": sys.version.split()[0], "platform": platform.platform()},
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
        "# Teklif ve Maliyet Araç Durumu",
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
