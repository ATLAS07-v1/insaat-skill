#!/usr/bin/env python3
import argparse
import csv
import difflib
import json
import re
from pathlib import Path


CODE_FIELDS = ["code", "mahal_no", "mahal_kodu", "room_no", "room_number", "number", "no", "id"]
NAME_FIELDS = ["name", "mahal_adi", "mahal", "room_name", "space_name", "oda_adi"]
LEVEL_FIELDS = ["level", "kat", "floor", "storey", "story", "seviye"]
AREA_FIELDS = ["area", "area_m2", "net_area", "net_area_m2", "net_alan", "net_alan_m2", "alan", "alan_m2"]
VOLUME_FIELDS = ["volume", "volume_m3", "hacim", "hacim_m3"]
COUNT_FIELDS = ["count", "adet", "quantity", "qty"]


def normalize_text(value):
    value = "" if value is None else str(value)
    value = value.strip().lower()
    value = value.replace("ı", "i").replace("İ", "i")
    value = re.sub(r"[^a-z0-9çğıöşü]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def parse_number(value):
    if value is None or value == "":
        return None
    text = str(value).strip().replace(" ", "")
    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    else:
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def pick(row, fields):
    lowered = {str(k).strip().lower(): v for k, v in row.items()}
    for field in fields:
        if field in lowered:
            return lowered[field]
    return None


def load_rows(path):
    path = Path(path)
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("rooms") or data.get("spaces") or data.get("items") or data.get("records") or []
        if not isinstance(data, list):
            raise ValueError("JSON input must be a list or contain rooms/spaces/items/records list")
        return data
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def normalize_row(row, source, index):
    code = pick(row, CODE_FIELDS)
    name = pick(row, NAME_FIELDS)
    level = pick(row, LEVEL_FIELDS)
    area = parse_number(pick(row, AREA_FIELDS))
    volume = parse_number(pick(row, VOLUME_FIELDS))
    count = parse_number(pick(row, COUNT_FIELDS))
    record = {
        "source": source,
        "index": index,
        "code": "" if code is None else str(code).strip(),
        "name": "" if name is None else str(name).strip(),
        "level": "" if level is None else str(level).strip(),
        "area_m2": area,
        "volume_m3": volume,
        "count": count,
        "normalized_name": normalize_text(name),
        "qa_flags": [],
        "raw": row,
    }
    if not record["code"] and not record["name"]:
        record["qa_flags"].append("missing_code_and_name")
    if not record["level"]:
        record["qa_flags"].append("missing_level")
    if area is not None and area <= 0:
        record["qa_flags"].append("non_positive_area")
    if volume is not None and volume <= 0:
        record["qa_flags"].append("non_positive_volume")
    if count is not None and count < 0:
        record["qa_flags"].append("negative_count")
    return record


def key_for(record):
    if record["code"]:
        return f'{normalize_text(record["level"])}|code:{normalize_text(record["code"])}'
    return f'{normalize_text(record["level"])}|name:{record["normalized_name"]}'


def index_records(records):
    index = {}
    duplicates = []
    for record in records:
        key = key_for(record)
        if key in index:
            duplicates.append(key)
            record["qa_flags"].append("duplicate_key")
            index[key]["qa_flags"].append("duplicate_key")
        else:
            index[key] = record
    return index, duplicates


def within_area_tolerance(a, b, abs_tol, pct_tol):
    if a is None or b is None:
        return False
    delta = abs(a - b)
    base = max(abs(a), abs(b), 1e-9)
    return delta <= max(abs_tol, base * pct_tol / 100.0)


def compare_values(a, b, abs_tol, pct_tol):
    if a is None and b is None:
        return None
    if a is None or b is None:
        return {"delta": None, "delta_percent": None, "over_tolerance": True, "missing_value": True}
    delta = b - a
    base = max(abs(a), 1e-9)
    return {
        "delta": round(delta, 6),
        "delta_percent": round(delta / base * 100, 6),
        "over_tolerance": not within_area_tolerance(a, b, abs_tol, pct_tol),
        "missing_value": False,
    }


def best_name_candidate(record, candidates):
    choices = []
    for key, candidate in candidates.items():
        if normalize_text(candidate["level"]) == normalize_text(record["level"]):
            choices.append((key, candidate))
    if not choices:
        choices = list(candidates.items())
    scored = []
    for key, candidate in choices:
        score = difflib.SequenceMatcher(None, record["normalized_name"], candidate["normalized_name"]).ratio() * 100
        scored.append((score, key, candidate))
    scored.sort(reverse=True, key=lambda item: item[0])
    return scored[0] if scored else None


def main():
    parser = argparse.ArgumentParser(description="Compare two room/space schedules in CSV or JSON.")
    parser.add_argument("--source-a", required=True)
    parser.add_argument("--source-b", required=True)
    parser.add_argument("--area-abs-tol", type=float, default=0.1)
    parser.add_argument("--area-pct-tol", type=float, default=1.0)
    parser.add_argument("--fuzzy-threshold", type=float, default=82.0)
    args = parser.parse_args()

    records_a = [normalize_row(row, "A", i + 1) for i, row in enumerate(load_rows(args.source_a))]
    records_b = [normalize_row(row, "B", i + 1) for i, row in enumerate(load_rows(args.source_b))]
    index_a, duplicates_a = index_records(records_a)
    index_b, duplicates_b = index_records(records_b)

    matches = []
    issues = []
    used_b = set()

    for key, rec_a in index_a.items():
        rec_b = index_b.get(key)
        match_method = "exact_key"
        confidence = 100.0
        if rec_b is None and rec_a["normalized_name"]:
            candidate = best_name_candidate(rec_a, {k: v for k, v in index_b.items() if k not in used_b})
            if candidate and candidate[0] >= args.fuzzy_threshold:
                confidence, candidate_key, rec_b = candidate
                key = candidate_key
                match_method = "fuzzy_name"
        if rec_b is None:
            issues.append({"type": "missing_in_source_b", "source_a": rec_a})
            continue
        used_b.add(key)
        area_check = compare_values(rec_a["area_m2"], rec_b["area_m2"], args.area_abs_tol, args.area_pct_tol)
        volume_check = compare_values(rec_a["volume_m3"], rec_b["volume_m3"], args.area_abs_tol, args.area_pct_tol)
        count_check = None
        if rec_a["count"] is not None or rec_b["count"] is not None:
            count_check = {
                "delta": None if rec_a["count"] is None or rec_b["count"] is None else rec_b["count"] - rec_a["count"],
                "over_tolerance": rec_a["count"] != rec_b["count"],
            }
        flags = []
        if area_check and area_check["over_tolerance"]:
            flags.append("area_delta_over_tolerance")
        if volume_check and volume_check["over_tolerance"]:
            flags.append("volume_delta_over_tolerance")
        if count_check and count_check["over_tolerance"]:
            flags.append("count_delta")
        if match_method == "fuzzy_name":
            flags.append("low_confidence_match")
        if normalize_text(rec_a["level"]) != normalize_text(rec_b["level"]):
            flags.append("level_mismatch")
        matches.append({
            "key": key,
            "match_method": match_method,
            "confidence": round(confidence, 3),
            "source_a": {k: rec_a[k] for k in ["code", "name", "level", "area_m2", "volume_m3", "count", "qa_flags"]},
            "source_b": {k: rec_b[k] for k in ["code", "name", "level", "area_m2", "volume_m3", "count", "qa_flags"]},
            "area_check": area_check,
            "volume_check": volume_check,
            "count_check": count_check,
            "flags": flags,
        })
        for flag in flags:
            if flag.endswith("over_tolerance") or flag in {"count_delta", "level_mismatch", "low_confidence_match"}:
                issues.append({"type": flag, "key": key, "source_a_name": rec_a["name"], "source_b_name": rec_b["name"]})

    for key, rec_b in index_b.items():
        if key not in used_b and key not in index_a:
            issues.append({"type": "missing_in_source_a", "source_b": rec_b})

    qa_flags = sorted({flag for record in records_a + records_b for flag in record["qa_flags"]})
    if duplicates_a:
        qa_flags.append("duplicates_in_source_a")
    if duplicates_b:
        qa_flags.append("duplicates_in_source_b")

    result = {
        "summary": {
            "source_a_count": len(records_a),
            "source_b_count": len(records_b),
            "matched_count": len(matches),
            "issue_count": len(issues),
            "source_a_area_total_m2": round(sum(r["area_m2"] or 0 for r in records_a), 6),
            "source_b_area_total_m2": round(sum(r["area_m2"] or 0 for r in records_b), 6),
        },
        "tolerances": {"area_abs_tol_m2": args.area_abs_tol, "area_pct_tol": args.area_pct_tol},
        "matches": matches,
        "issues": issues,
        "qa_flags": sorted(set(qa_flags)),
    }
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
