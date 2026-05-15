#!/usr/bin/env python3
"""Report available tools for technical specification and site QA workflows."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
import sys
from typing import Any


MODULES = {
    "pandas": "Tabular QA, evidence registers, test result summaries",
    "openpyxl": "XLSX schedules and submittal registers",
    "pdfplumber": "PDF text and table extraction",
    "pypdf": "Pure Python PDF text extraction fallback",
    "fitz": "PyMuPDF PDF extraction and rendering fallback",
    "docx": "python-docx for DOCX specifications and tables",
    "jsonschema": "Machine-readable output schema validation",
    "yaml": "YAML rule and agent metadata parsing",
    "rapidfuzz": "Fuzzy matching between clauses and evidence titles",
    "great_expectations": "Data-quality style validation for large registers",
    "ifcopenshell": "IFC model inspection",
    "ifctester": "IDS validation against IFC models",
}

COMMANDS = {
    "python": "Python runtime",
    "pip": "Python package installer",
    "ifctester": "IDS command-line validation",
    "gherkin": "Gherkin parser/CLI for executable specification patterns",
    "pandoc": "Document conversion fallback",
    "qpdf": "PDF repair and metadata inspection",
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
            {
                "name": name,
                "available": module_available(name),
                "purpose": purpose,
            }
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
        "# Teknik Şartname Araç Durumu",
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
    if args.format == "markdown":
        print(to_markdown(report))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
