#!/usr/bin/env python3
"""Report local tool availability for construction communication drafting workflows."""

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
    ModuleCheck("pandas", "pandas", "iletişim, aksiyon ve takip tabloları"),
    ModuleCheck("openpyxl", "openpyxl", "XLSX okuma/yazma"),
    ModuleCheck("xlsxwriter", "XlsxWriter", "XLSX aksiyon listesi üretimi"),
    ModuleCheck("yaml", "PyYAML", "YAML şablon/konfigürasyon okuma"),
    ModuleCheck("jinja2", "Jinja2", "mesaj ve belge şablonlama"),
    ModuleCheck("markdown", "Markdown", "Markdown dönüştürme"),
    ModuleCheck("docx", "python-docx", "DOCX tutanak/yazı üretimi"),
    ModuleCheck("pypdf", "pypdf", "PDF metin kontrolü"),
    ModuleCheck("pdfplumber", "pdfplumber", "PDF tablo/metin çıkarımı"),
    ModuleCheck("rapidfuzz", "RapidFuzz", "alıcı, konu ve referans eşleştirme"),
    ModuleCheck("requests", "requests", "CRM/helpdesk API entegrasyonu"),
    ModuleCheck("bs4", "BeautifulSoup", "HTML kaynak ayrıştırma"),
    ModuleCheck("email_validator", "email-validator", "e-posta adres doğrulama"),
]

COMMANDS = [
    CommandCheck("python", "Python", "yerel script çalıştırma"),
    CommandCheck("pip", "pip", "paket kurulum ve inceleme"),
    CommandCheck("git", "git", "açık kaynak repo inceleme"),
    CommandCheck("pandoc", "Pandoc", "Markdown/DOCX/PDF dönüşümü"),
    CommandCheck("soffice", "LibreOffice", "ofis dosyası dönüşümü"),
    CommandCheck("libreoffice", "LibreOffice", "ofis dosyası dönüşümü"),
]


def module_available(import_name: str) -> bool:
    return importlib.util.find_spec(import_name) is not None


def command_version(command: str) -> str | None:
    if shutil.which(command) is None:
        return None
    for args in ([command, "--version"], [command, "-V"], [command, "-h"]):
        try:
            completed = subprocess.run(args, capture_output=True, text=True, timeout=4)
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
            "pandas",
            "xlsxwriter",
            "jinja2 for reusable templates",
            "python-docx or pandoc for formal document output",
            "requests for CRM/helpdesk API integrations",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = ["# İletişim Hazırlayıcı Araç Durumu", ""]
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
