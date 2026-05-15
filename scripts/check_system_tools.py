#!/usr/bin/env python3
"""Report Python dependency and system tool availability for selected skills."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

PYTHON_GROUPS = {
    "core": {
        "required": True,
        "modules": {
            "yaml": "PyYAML",
            "PIL": "Pillow",
            "pypdf": "pypdf",
            "pandas": "pandas",
            "xlsxwriter": "XlsxWriter",
            "requests": "requests",
            "bs4": "beautifulsoup4",
            "jsonschema": "jsonschema",
        },
    },
    "cad": {"required": False, "modules": {"ezdxf": "ezdxf"}},
    "bim": {"required": False, "modules": {"ifcopenshell": "ifcopenshell"}},
    "pdf-doc": {
        "required": False,
        "modules": {
            "docx": "python-docx",
            "pdfplumber": "pdfplumber",
            "fitz": "PyMuPDF",
            "markdown": "markdown",
            "odf": "odfpy",
            "lxml": "lxml",
        },
    },
    "spreadsheet": {"required": False, "modules": {"openpyxl": "openpyxl", "numpy": "numpy"}},
    "image-ocr": {
        "required": False,
        "modules": {
            "cv2": "opencv-python",
            "imagehash": "imagehash",
            "pytesseract": "pytesseract",
            "skimage": "scikit-image",
            "exifread": "exifread",
            "piexif": "piexif",
            "rawpy": "rawpy",
            "geopandas": "geopandas",
        },
    },
    "data-quality": {
        "required": False,
        "modules": {
            "jsonschema": "jsonschema",
            "frictionless": "frictionless",
            "great_expectations": "great-expectations",
            "rapidfuzz": "rapidfuzz",
        },
    },
    "communication": {"required": False, "modules": {"jinja2": "Jinja2", "email_validator": "email-validator"}},
    "dev": {"required": False, "modules": {"pytest": "pytest", "jsonschema": "jsonschema"}},
}

SYSTEM_TOOL_CATALOG = {
    "Pandoc": {"commands": ["pandoc"], "category": "optional_open_source_cli"},
    "LibreOffice": {"commands": ["soffice", "libreoffice"], "category": "optional_open_source_cli"},
    "qpdf": {"commands": ["qpdf"], "category": "optional_open_source_cli"},
    "ExifTool": {"commands": ["exiftool"], "category": "optional_open_source_cli"},
    "Tesseract OCR": {"commands": ["tesseract"], "category": "optional_open_source_cli"},
    "ImageMagick": {"commands": ["magick", "convert"], "category": "optional_open_source_cli"},
    "FFmpeg": {"commands": ["ffmpeg"], "category": "optional_open_source_cli"},
    "Blender": {"commands": ["blender"], "category": "optional_open_source_cli"},
    "SketchUp": {"commands": ["SketchUp", "SketchUp.exe"], "category": "manual_install_required"},
    "IfcConvert": {"commands": ["IfcConvert", "ifcconvert"], "category": "optional_open_source_cli"},
    "IfcTester CLI": {"commands": ["ifctester"], "category": "optional_open_source_cli"},
    "BlenderBIM": {"commands": ["blender"], "category": "optional_open_source_cli"},
    "ODA File Converter": {"commands": ["ODAFileConverter", "ODAFileConverter.exe"], "category": "manual_install_required"},
    "LibreDWG": {"commands": ["dwg2dxf", "dwgread"], "category": "optional_open_source_cli"},
    "QCAD or LibreCAD": {"commands": ["qcad", "librecad"], "category": "optional_open_source_cli"},
    "OpenRefine": {"commands": ["openrefine"], "category": "optional_open_source_cli"},
    "OpenSCAP": {"commands": ["oscap"], "category": "optional_open_source_cli"},
    "QGIS": {"commands": ["qgis", "qgis-bin"], "category": "optional_open_source_cli"},
    "Docker": {"commands": ["docker"], "category": "optional_open_source_cli"},
    "Java": {"commands": ["java"], "category": "optional_open_source_cli"},
    "Node.js": {"commands": ["node"], "category": "optional_open_source_cli"},
}


def load_index(source_root: Path) -> dict[str, Any]:
    return json.loads((source_root / "skill-index.json").read_text(encoding="utf-8-sig"))


def selected_skill_items(index: dict[str, Any], selected: list[str]) -> list[dict[str, Any]]:
    skills = [item for item in index.get("skills", []) if isinstance(item, dict)]
    by_name = {item["name"]: item for item in skills if item.get("name")}
    if not selected:
        return skills
    unknown = sorted(set(selected) - set(by_name))
    if unknown:
        raise SystemExit(f"Unknown skill(s): {', '.join(unknown)}")
    return [by_name[name] for name in selected]


def module_available(module: str) -> bool:
    return importlib.util.find_spec(module) is not None


def command_candidates(candidates: list[str]) -> tuple[bool, str | None]:
    for command in candidates:
        path = shutil.which(command)
        if path:
            return True, path
    return False, None


def status_for(available: bool, required: bool, manual: bool = False) -> str:
    if available:
        return "available"
    if manual:
        return "manual_install_required"
    return "missing_required" if required else "missing_optional"


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    source_root = Path(args.source_root).resolve()
    index = load_index(source_root)
    items = selected_skill_items(index, args.skill or [])
    dependency_groups = sorted({group for item in items for group in item.get("dependency_groups", [])})
    system_tools = sorted({tool for item in items for tool in item.get("system_tools", [])})

    python_modules = []
    seen_modules: set[str] = set()
    for group in dependency_groups:
        group_meta = PYTHON_GROUPS.get(group)
        if not group_meta:
            python_modules.append(
                {"group": group, "module": "", "package": "", "status": "unknown_group", "available": False}
            )
            continue
        required = bool(group_meta["required"])
        for module, package in group_meta["modules"].items():
            key = f"{group}:{module}"
            if key in seen_modules:
                continue
            seen_modules.add(key)
            available = module_available(module)
            python_modules.append(
                {
                    "group": group,
                    "module": module,
                    "package": package,
                    "required": required,
                    "available": available,
                    "status": status_for(available, required),
                }
            )

    commands = []
    for tool in system_tools:
        meta = SYSTEM_TOOL_CATALOG.get(tool, {"commands": [tool], "category": "manual_install_required"})
        available, path = command_candidates(meta["commands"])
        manual = meta["category"] == "manual_install_required"
        commands.append(
            {
                "tool": tool,
                "commands": meta["commands"],
                "category": meta["category"],
                "available": available,
                "path": path,
                "status": status_for(available, required=False, manual=manual),
            }
        )

    blocking = [item for item in python_modules + commands if item["status"] == "missing_required"]
    return {
        "status": "ok" if not blocking else "blocked",
        "source_root": str(source_root),
        "selected_skills": [item["name"] for item in items],
        "dependency_groups": dependency_groups,
        "runtime": {"python": sys.version.split()[0], "platform": platform.platform()},
        "python_modules": python_modules,
        "system_tools": commands,
        "summary": {
            "skill_count": len(items),
            "python_module_count": len(python_modules),
            "system_tool_count": len(commands),
            "missing_required_count": len(blocking),
            "missing_optional_count": sum(1 for item in python_modules + commands if item["status"] == "missing_optional"),
            "manual_install_required_count": sum(
                1 for item in python_modules + commands if item["status"] == "manual_install_required"
            ),
        },
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# System Tool Check",
        "",
        f"- Status: {payload['status']}",
        f"- Skills: {payload['summary']['skill_count']}",
        f"- Python: {payload['runtime']['python']}",
        "",
        "## Python Modules",
        "",
        "| Group | Module | Package | Status |",
        "|---|---|---|---|",
    ]
    for item in payload["python_modules"]:
        lines.append(f"| `{item['group']}` | `{item['module']}` | `{item['package']}` | {item['status']} |")
    lines.extend(["", "## System Tools", "", "| Tool | Status | Path | Category |", "|---|---|---|---|"])
    for item in payload["system_tools"]:
        lines.append(f"| `{item['tool']}` | {item['status']} | `{item['path'] or '-'}` | {item['category']} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", default=str(ROOT), help="Repository or package root containing skill-index.json.")
    parser.add_argument("--skill", action="append", help="Skill name to scope the report. Repeat for multiple skills.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    payload = build_report(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
