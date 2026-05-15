#!/usr/bin/env python3
"""Inspect a DXF file with ezdxf and emit a compact JSON report."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def point_tuple(point) -> list[float]:
    try:
        return [float(point.x), float(point.y), float(point.z)]
    except Exception:
        try:
            return [float(point[0]), float(point[1]), float(point[2] if len(point) > 2 else 0.0)]
        except Exception:
            return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="DXF file")
    parser.add_argument("--max-texts", type=int, default=200)
    args = parser.parse_args()

    try:
        import ezdxf  # type: ignore
        from ezdxf import recover  # type: ignore
    except Exception:
        print("ezdxf is not installed. Install with: pip install ezdxf[draw]")
        return 2

    path = Path(args.path)
    try:
        doc = ezdxf.readfile(path)
        audit = doc.audit()
        recover_errors: list[str] = []
    except ezdxf.DXFStructureError:
        doc, auditor = recover.readfile(path)
        audit = auditor
        recover_errors = ["recover_mode_used"]

    entity_counts: Counter[str] = Counter()
    layer_counts: dict[str, int] = defaultdict(int)
    text_records: list[dict] = []
    insert_counts: Counter[str] = Counter()

    for layout in doc.layouts:
        for entity in layout:
            etype = entity.dxftype()
            entity_counts[etype] += 1
            layer = getattr(entity.dxf, "layer", "")
            layer_counts[layer] += 1
            if etype in {"TEXT", "MTEXT"} and len(text_records) < args.max_texts:
                text = entity.plain_text() if hasattr(entity, "plain_text") else getattr(entity.dxf, "text", "")
                insert = getattr(entity.dxf, "insert", None)
                text_records.append(
                    {
                        "layout": layout.name,
                        "layer": layer,
                        "type": etype,
                        "text": str(text).strip(),
                        "insert": point_tuple(insert) if insert is not None else [],
                    }
                )
            if etype == "INSERT":
                insert_counts[getattr(entity.dxf, "name", "")] += 1

    quality_flags: list[str] = []
    insunits = doc.header.get("$INSUNITS", None)
    if not insunits:
        quality_flags.append("missing_units")
    if entity_counts.get("ACAD_PROXY_ENTITY", 0):
        quality_flags.append("proxy_entity_present")
    if any(kind in entity_counts for kind in ["IMAGE", "UNDERLAY", "PDFUNDERLAY", "DGNUNDERLAY", "DWFUNDERLAY"]):
        quality_flags.append("underlay_or_image_present")

    result = {
        "source_file": str(path.resolve()),
        "file_type": "dxf",
        "dxf_version": doc.dxfversion,
        "insunits": insunits,
        "layouts": [layout.name for layout in doc.layouts],
        "layers": [
            {"name": name, "entity_count": count}
            for name, count in sorted(layer_counts.items(), key=lambda item: item[0].lower())
        ],
        "blocks": [
            {"name": name, "insert_count": count}
            for name, count in sorted(insert_counts.items(), key=lambda item: item[0].lower())
        ],
        "entities": dict(entity_counts),
        "texts": text_records,
        "audit": {
            "errors": len(getattr(audit, "errors", [])),
            "fixes": len(getattr(audit, "fixes", [])),
            "recover": recover_errors,
        },
        "quality_flags": quality_flags,
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
