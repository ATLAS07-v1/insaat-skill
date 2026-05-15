#!/usr/bin/env python3
"""Report local tool availability for construction risk, safety, and compliance audits."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ModuleCheck:
    import_name: str
    label: str
    purpose: str


@dataclass(frozen=True)
class CommandCheck:
    command: str
    label: str
    purpose: str


MODULES = [
    ModuleCheck("pandas", "pandas", "tablo ve risk register analizi"),
    ModuleCheck("numpy", "numpy", "sayısal analiz ve matris işlemleri"),
    ModuleCheck("openpyxl", "openpyxl", "XLSX okuma/yazma"),
    ModuleCheck("xlsxwriter", "XlsxWriter", "XLSX rapor üretimi"),
    ModuleCheck("yaml", "PyYAML", "YAML kontrol kataloğu okuma"),
    ModuleCheck("jsonschema", "jsonschema", "JSON şema doğrulama"),
    ModuleCheck("frictionless", "Frictionless", "CSV/veri paketi kalite kontrolü"),
    ModuleCheck("great_expectations", "Great Expectations", "veri kalite beklenti testleri"),
    ModuleCheck("pypdf", "pypdf", "PDF metin çıkarımı"),
    ModuleCheck("pdfplumber", "pdfplumber", "PDF tablo/metin çıkarımı"),
    ModuleCheck("docx", "python-docx", "DOCX method statement ve tutanak okuma"),
    ModuleCheck("rapidfuzz", "RapidFuzz", "madde ve belge eşleştirme"),
    ModuleCheck("ifcopenshell", "IfcOpenShell", "IFC model okuma"),
    ModuleCheck("ifctester", "IfcTester", "IDS tabanlı IFC uygunluk denetimi"),
    ModuleCheck("requests", "requests", "web/API kaynak kontrolü"),
    ModuleCheck("bs4", "BeautifulSoup", "HTML kaynak ayrıştırma"),
]

COMMANDS = [
    CommandCheck("python", "Python", "yerel script çalıştırma"),
    CommandCheck("pip", "pip", "paket kurulum ve inceleme"),
    CommandCheck("soffice", "LibreOffice", "ofis dosyası dönüşümü"),
    CommandCheck("libreoffice", "LibreOffice", "ofis dosyası dönüşümü"),
    CommandCheck("qpdf", "qpdf", "PDF doğrulama ve onarım"),
    CommandCheck("ifctester", "IfcTester CLI", "IDS/IFC komut satırı denetimi"),
    CommandCheck("oscap", "OpenSCAP oscap", "uyumluluk-as-code taraması"),
]


def module_available(import_name: str) -> bool:
    return importlib.util.find_spec(import_name) is not None


def command_version(command: str) -> str | None:
    path = shutil.which(command)
    if not path:
        return None
    for args in ([command, "--version"], [command, "-V"], [command, "-h"]):
        try:
            completed = subprocess.run(args, capture_output=True, text=True, timeout=4)
        except (OSError, subprocess.SubprocessError):
            continue
        output = (completed.stdout or completed.stderr or "").strip().splitlines()
        if output:
            return output[0][:160]
    return path


def collect() -> dict[str, Any]:
    modules = [
        {
            "label": item.label,
            "import_name": item.import_name,
            "purpose": item.purpose,
            "available": module_available(item.import_name),
        }
        for item in MODULES
    ]
    commands = [
        {
            "label": item.label,
            "command": item.command,
            "purpose": item.purpose,
            "available": shutil.which(item.command) is not None,
            "version": command_version(item.command),
        }
        for item in COMMANDS
    ]
    return {
        "summary": {
            "available_modules": sum(1 for item in modules if item["available"]),
            "total_modules": len(modules),
            "available_commands": sum(1 for item in commands if item["available"]),
            "total_commands": len(commands),
        },
        "modules": modules,
        "commands": commands,
        "recommended_minimum": [
            "python",
            "pandas",
            "xlsxwriter",
            "pypdf",
            "frictionless or jsonschema",
            "ifcopenshell and ifctester for IFC/IDS audits",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = ["# Risk / Güvenlik / Uygunluk Araç Durumu", ""]
    summary = payload["summary"]
    lines.append(
        f"- Python modülleri: {summary['available_modules']} / {summary['total_modules']} kullanılabilir"
    )
    lines.append(
        f"- Komut satırı araçları: {summary['available_commands']} / {summary['total_commands']} kullanılabilir"
    )
    lines.extend(["", "## Python Modülleri", "", "| Araç | Durum | Amaç |", "|---|---|---|"])
    for item in payload["modules"]:
        status = "var" if item["available"] else "yok"
        lines.append(f"| {item['label']} | {status} | {item['purpose']} |")
    lines.extend(["", "## Komutlar", "", "| Komut | Durum | Amaç | Sürüm / Not |", "|---|---|---|---|"])
    for item in payload["commands"]:
        status = "var" if item["available"] else "yok"
        version = item["version"] or ""
        lines.append(f"| {item['command']} | {status} | {item['purpose']} | {version} |")
    lines.extend(["", "## Önerilen Minimum", ""])
    for item in payload["recommended_minimum"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    payload = collect()
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
