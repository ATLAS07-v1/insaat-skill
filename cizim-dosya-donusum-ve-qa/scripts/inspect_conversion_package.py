#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


TEXT_EXTS = {".dxf", ".ifc", ".obj", ".svg", ".gltf", ".stl", ".step", ".stp", ".iges", ".igs"}
PROPRIETARY_EXTS = {".rvt", ".skp", ".dwg", ".fbx"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_sample(path, size=1024 * 1024):
    with open(path, "rb") as fh:
        return fh.read(size)


def classify(path, data):
    ext = path.suffix.lower()
    text = None
    if ext in TEXT_EXTS:
        try:
            text = data.decode("utf-8", errors="ignore")
        except Exception:
            text = ""

    if data.startswith(b"%PDF"):
        return "pdf", "pdf_header", {}
    if data.startswith(b"AC10"):
        return "cad_dwg", data[:6].decode("ascii", errors="ignore"), {}
    if data.startswith(b"glTF"):
        return "gltf_glb", "glb_magic", {}
    if data.startswith(b"PK\x03\x04"):
        return "zip_based_or_archive", "zip_magic", {}
    if text is not None:
        upper = text[:200000].upper()
        if ext == ".dxf" or "SECTION" in upper and "ENTITIES" in upper:
            return "cad_dxf", "text_dxf", {"dxf_sections": len(re.findall(r"\bSECTION\b", upper))}
        if "ISO-10303-21" in upper and (ext in {".ifc", ".step", ".stp", ".iges", ".igs"}):
            entity_count = len(re.findall(r"#\d+\s*=", text))
            if ext == ".ifc":
                return "bim_ifc", "iso_10303_21", {"step_entity_count_sample": entity_count}
            if ext in {".step", ".stp"}:
                return "solid_step", "iso_10303_21", {"step_entity_count_sample": entity_count}
            return "solid_iges", "iso_10303_21", {"step_entity_count_sample": entity_count}
        if ext == ".obj" or re.search(r"(?m)^v\s+", text):
            return "mesh_obj", "text_obj", {
                "obj_vertices_sample": len(re.findall(r"(?m)^v\s+", text)),
                "obj_faces_sample": len(re.findall(r"(?m)^f\s+", text)),
            }
        if ext == ".svg" or "<svg" in text[:2000].lower():
            return "vector_svg", "text_svg", {}
        if ext == ".stl" and text.lstrip().lower().startswith("solid"):
            return "mesh_stl_ascii", "text_stl", {}
    return "unknown_or_binary", "unknown", {}


def inspect_file(path):
    info = {
        "path": str(path),
        "name": path.name,
        "extension": path.suffix.lower(),
        "exists": path.exists(),
        "qa_flags": [],
    }
    if not path.exists():
        info["qa_flags"].append("missing_file")
        return info
    if path.is_dir():
        info["qa_flags"].append("directory_not_file")
        return info

    size = path.stat().st_size
    info["size_bytes"] = size
    if size == 0:
        info["qa_flags"].append("zero_byte_file")
        return info
    if size > 500 * 1024 * 1024:
        info["qa_flags"].append("large_file_over_500mb")

    info["sha256"] = sha256(path)
    sample = read_sample(path)
    kind, magic, extra = classify(path, sample)
    info["detected_kind"] = kind
    info["magic"] = magic
    info.update(extra)

    ext = path.suffix.lower()
    if ext in PROPRIETARY_EXTS:
        info["qa_flags"].append("proprietary_or_lossy_conversion_risk")
    if ext == ".pdf" and magic != "pdf_header":
        info["qa_flags"].append("pdf_extension_without_pdf_header")
    if ext == ".dxf" and kind != "cad_dxf":
        info["qa_flags"].append("dxf_extension_without_basic_dxf_markers")
    if ext in {".glb", ".gltf"}:
        info["qa_flags"].append("run_gltf_validator")
    if kind == "unknown_or_binary":
        info["qa_flags"].append("needs_tool_specific_inspection")
    return info


def collect_paths(items):
    files = []
    for item in items:
        path = Path(item)
        if path.is_dir():
            files.extend([p for p in path.rglob("*") if p.is_file()])
        else:
            files.append(path)
    return files


def main():
    parser = argparse.ArgumentParser(description="Inspect drawing/model conversion packages.")
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()

    records = [inspect_file(path) for path in collect_paths(args.paths)]
    kinds = Counter(record.get("detected_kind", "unknown") for record in records)
    risk_count = sum(1 for record in records if record.get("qa_flags"))
    result = {
        "files": records,
        "summary": {
            "file_count": len(records),
            "risk_count": risk_count,
            "kinds": dict(kinds),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
