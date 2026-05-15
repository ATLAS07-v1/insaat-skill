#!/usr/bin/env python3
"""Report local tool availability for document standardization and formatting."""

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
    ModuleCheck("docx", "python-docx", "DOCX oluşturma ve düzenleme"),
    ModuleCheck("pypdf", "pypdf", "PDF okuma, sayfa sayısı ve birleştirme"),
    ModuleCheck("fitz", "PyMuPDF", "PDF render/metin kontrolü"),
    ModuleCheck("openpyxl", "openpyxl", "XLSX manifest ve tablo üretimi"),
    ModuleCheck("xlsxwriter", "XlsxWriter", "XLSX rapor üretimi"),
    ModuleCheck("pandas", "pandas", "doküman register analizi"),
    ModuleCheck("yaml", "PyYAML", "YAML şablon ve konfigürasyon"),
    ModuleCheck("jinja2", "Jinja2", "doküman şablonlama"),
    ModuleCheck("lxml", "lxml", "OOXML/XML ayrıştırma"),
    ModuleCheck("markdown", "Markdown", "Markdown dönüştürme"),
    ModuleCheck("bs4", "BeautifulSoup", "HTML kontrolü"),
    ModuleCheck("odf", "odfpy", "ODF/ODT işlem desteği"),
]

COMMANDS = [
    CommandCheck("python", "Python", "yerel script çalıştırma"),
    CommandCheck("pip", "pip", "paket kurulum ve inceleme"),
    CommandCheck("pandoc", "Pandoc", "çok formatlı belge dönüşümü"),
    CommandCheck("soffice", "LibreOffice", "headless Office/PDF dönüşümü"),
    CommandCheck("libreoffice", "LibreOffice", "headless Office/PDF dönüşümü"),
    CommandCheck("qpdf", "qpdf", "PDF doğrulama/onarım"),
    CommandCheck("java", "Java", "LanguageTool, Apache POI, docx4j çalıştırma"),
    CommandCheck("node", "Node.js", "markdownlint, Prettier, remark-lint"),
    CommandCheck("npm", "npm", "Node tabanlı lint/format araçları"),
    CommandCheck("prettier", "Prettier", "Markdown/YAML/JSON formatlama"),
    CommandCheck("markdownlint-cli2", "markdownlint-cli2", "Markdown lint"),
    CommandCheck("vale", "Vale", "prose/style lint"),
    CommandCheck("languagetool", "LanguageTool", "dilbilgisi ve stil kontrolü"),
]


def module_available(import_name: str) -> bool:
    return importlib.util.find_spec(import_name) is not None


def command_version(command: str) -> str | None:
    if shutil.which(command) is None:
        return None
    for args in ([command, "--version"], [command, "-version"], [command, "-v"], [command, "-h"]):
        try:
            completed = subprocess.run(args, capture_output=True, text=True, timeout=5)
        except (OSError, subprocess.SubprocessError):
            continue
        output = (completed.stdout or completed.stderr or "").strip().splitlines()
        if output:
            return output[0][:160]
    return shutil.which(command)


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
            "pandoc",
            "pypdf",
            "python-docx for DOCX generation",
            "LibreOffice for Office-to-PDF conversion",
            "Vale or markdownlint for document style QA",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = ["# Doküman Format Araç Durumu", ""]
    lines.append(f"- Python modülleri: {summary['available_modules']} / {summary['total_modules']} kullanılabilir")
    lines.append(f"- Komut satırı araçları: {summary['available_commands']} / {summary['total_commands']} kullanılabilir")
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
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
