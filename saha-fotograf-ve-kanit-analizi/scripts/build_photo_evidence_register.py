#!/usr/bin/env python3
"""Build a photo evidence register with file hashes and basic metadata."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".bmp", ".gif", ".heic", ".heif"}

try:
    from PIL import Image, ExifTags
except Exception:  # pragma: no cover - optional dependency
    Image = None
    ExifTags = None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iso_from_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_exif_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(text, fmt).isoformat()
        except ValueError:
            continue
    return text


def read_image_metadata(path: Path) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "width": None,
        "height": None,
        "exif_present": False,
        "gps_present": False,
        "captured_at": "",
        "camera_make": "",
        "camera_model": "",
    }
    if Image is None:
        return metadata
    try:
        with Image.open(path) as image:
            metadata["width"], metadata["height"] = image.size
            raw_exif = image.getexif()
            if raw_exif:
                metadata["exif_present"] = True
                tag_names = ExifTags.TAGS if ExifTags else {}
                for tag_id, value in raw_exif.items():
                    tag = tag_names.get(tag_id, str(tag_id))
                    if tag in {"DateTimeOriginal", "DateTimeDigitized", "DateTime"} and not metadata["captured_at"]:
                        metadata["captured_at"] = normalize_exif_date(value)
                    elif tag == "Make":
                        metadata["camera_make"] = str(value)
                    elif tag == "Model":
                        metadata["camera_model"] = str(value)
                    elif tag == "GPSInfo":
                        metadata["gps_present"] = True
    except Exception:
        metadata["read_error"] = "image_metadata_read_failed"
    return metadata


def scan_folder(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.folder).expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"Klasör bulunamadı: {root}")
    files = [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    rows = []
    for index, path in enumerate(sorted(files), start=1):
        stat = path.stat()
        image_meta = read_image_metadata(path)
        evidence_id = f"{args.id_prefix}-{index:04d}"
        rows.append(
            {
                "evidence_id": evidence_id,
                "file_path": str(path),
                "file_name": path.name,
                "extension": path.suffix.lower(),
                "sha256": sha256_file(path),
                "file_size": stat.st_size,
                "modified_at": iso_from_timestamp(stat.st_mtime),
                "captured_at": image_meta.get("captured_at") or "",
                "width": image_meta.get("width"),
                "height": image_meta.get("height"),
                "exif_present": bool(image_meta.get("exif_present")),
                "gps_present": bool(image_meta.get("gps_present")),
                "camera_make": image_meta.get("camera_make") or "",
                "camera_model": image_meta.get("camera_model") or "",
                "project": args.project or "",
                "location": args.location or "",
                "subject": args.subject or "",
                "source": args.source or "",
                "tags": [tag.strip() for tag in (args.tag or []) if tag.strip()],
                "notes": image_meta.get("read_error", ""),
            }
        )
    return {
        "summary": {
            "folder": str(root),
            "photo_count": len(rows),
            "generated_at": datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z"),
        },
        "photos": rows,
    }


def write_csv(payload: dict[str, Any], output: Path) -> None:
    rows = payload["photos"]
    fieldnames = [
        "evidence_id",
        "file_path",
        "file_name",
        "extension",
        "sha256",
        "file_size",
        "modified_at",
        "captured_at",
        "width",
        "height",
        "exif_present",
        "gps_present",
        "camera_make",
        "camera_model",
        "project",
        "location",
        "subject",
        "source",
        "tags",
        "notes",
    ]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            clean = dict(row)
            clean["tags"] = ";".join(row.get("tags") or [])
            writer.writerow(clean)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder")
    parser.add_argument("--project")
    parser.add_argument("--location")
    parser.add_argument("--subject")
    parser.add_argument("--source")
    parser.add_argument("--tag", action="append")
    parser.add_argument("--id-prefix", default="PH")
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    parser.add_argument("--output")
    args = parser.parse_args()
    payload = scan_folder(args)
    if args.output:
        output = Path(args.output)
        if args.format == "csv":
            write_csv(payload, output)
        else:
            output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
