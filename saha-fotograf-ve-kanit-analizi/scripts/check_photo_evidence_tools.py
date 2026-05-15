#!/usr/bin/env python3
"""Report local tool availability for construction photo/evidence analysis."""

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
    ModuleCheck("PIL", "Pillow", "görsel okuma, boyut ve temel EXIF"),
    ModuleCheck("cv2", "OpenCV", "görsel işleme ve kalite ön kontrolü"),
    ModuleCheck("numpy", "numpy", "görsel matris işlemleri"),
    ModuleCheck("pandas", "pandas", "kanıt register ve rapor tabloları"),
    ModuleCheck("yaml", "PyYAML", "YAML konfigürasyon okuma"),
    ModuleCheck("exifread", "exifread", "EXIF okuma fallback"),
    ModuleCheck("piexif", "piexif", "EXIF ayrıştırma/yazma"),
    ModuleCheck("pytesseract", "pytesseract", "Tesseract OCR Python köprüsü"),
    ModuleCheck("imagehash", "ImageHash", "perceptual hash ve near-duplicate"),
    ModuleCheck("skimage", "scikit-image", "görsel kalite ve analiz işlemleri"),
    ModuleCheck("rawpy", "rawpy", "RAW fotoğraf okuma"),
    ModuleCheck("geopandas", "GeoPandas", "geotag ve GIS veri işlemleri"),
    ModuleCheck("requests", "requests", "API entegrasyonları"),
]

COMMANDS = [
    CommandCheck("python", "Python", "yerel script çalıştırma"),
    CommandCheck("pip", "pip", "paket kurulum ve inceleme"),
    CommandCheck("exiftool", "ExifTool", "EXIF/IPTC/XMP metadata okuma"),
    CommandCheck("tesseract", "Tesseract OCR", "görselden metin çıkarımı"),
    CommandCheck("magick", "ImageMagick", "görsel dönüşüm ve ön işleme"),
    CommandCheck("ffmpeg", "FFmpeg", "video kare çıkarımı"),
    CommandCheck("git", "git", "açık kaynak repo inceleme"),
    CommandCheck("qgis", "QGIS", "GIS ve geotag görselleştirme"),
    CommandCheck("docker", "Docker", "CVAT, Label Studio, ODM gibi servisleri çalıştırma"),
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
            "Pillow",
            "pandas or CSV stdlib",
            "ExifTool for strong metadata extraction",
            "Tesseract for OCR",
            "ImageHash or OpenCV for duplicate/near-duplicate workflows",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = ["# Saha Fotoğraf / Kanıt Araç Durumu", ""]
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
