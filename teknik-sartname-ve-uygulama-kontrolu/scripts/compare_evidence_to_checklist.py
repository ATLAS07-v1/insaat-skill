#!/usr/bin/env python3
"""Compare extracted specification clauses with evidence records."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


PASS_VALUES = {"pass", "passed", "ok", "uygun", "geçti", "evet", "true", "closed"}
FAIL_VALUES = {"fail", "failed", "nok", "uygunsuz", "kaldı", "hayır", "false", "open"}
PENDING_VALUES = {"pending", "bekliyor", "review", "inceleme", "partial", "kısmi"}


def load_json_or_csv(path: Path) -> Any:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    if suffix in {".txt", ".md"}:
        return [{"id": path.stem, "text": path.read_text(encoding="utf-8", errors="replace")}]
    raise SystemExit(f"Desteklenmeyen kanıt veya kontrol listesi dosya türü: {suffix}")


def load_clauses(path: Path) -> list[dict[str, Any]]:
    data = load_json_or_csv(path)
    if isinstance(data, dict) and isinstance(data.get("clauses"), list):
        return data["clauses"]
    if isinstance(data, list):
        return data
    raise SystemExit("Kontrol listesi JSON içinde `clauses` listesi veya doğrudan liste olmalıdır.")


def load_evidence(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    if path.is_dir():
        records = []
        for file in sorted(p for p in path.iterdir() if p.is_file()):
            records.append(
                {
                    "id": file.stem,
                    "file": str(file),
                    "text": file.name,
                    "status": "pending",
                    "tags": re.split(r"[_\-\s.]+", file.stem.lower()),
                }
            )
        return records
    data = load_json_or_csv(path)
    if isinstance(data, dict):
        for key in ("evidence", "records", "items", "results"):
            if isinstance(data.get(key), list):
                return data[key]
        return [data]
    if isinstance(data, list):
        return data
    return []


def evidence_text(record: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ("id", "clause_id", "source_ref", "file", "title", "name", "text", "notes", "status", "result"):
        value = record.get(key)
        if value is None:
            continue
        if isinstance(value, list):
            parts.extend(str(item) for item in value)
        else:
            parts.append(str(value))
    return " ".join(parts).lower()


def normalize_status(value: Any) -> str:
    text = str(value or "").strip().lower()
    if text in PASS_VALUES:
        return "passed"
    if text in FAIL_VALUES:
        return "failed"
    if text in PENDING_VALUES:
        return "pending"
    return "unknown"


def matches_clause(clause: dict[str, Any], record: dict[str, Any]) -> bool:
    clause_id = str(clause.get("id", "")).lower()
    text = evidence_text(record)
    explicit = str(record.get("clause_id", "")).lower()
    if explicit and explicit == clause_id:
        return True
    if clause_id and clause_id in text:
        return True
    source_ref = str(clause.get("source_ref", "")).lower()
    if source_ref and source_ref in text:
        return True
    return False


def action_for(clause: dict[str, Any], status: str) -> str:
    required = ", ".join(clause.get("evidence_required") or ["inspection_record"])
    if status == "missing_evidence":
        return f"Gerekli kanıt istenmeli: {required}."
    if status == "failed":
        return "Uygunsuzluk/NCR veya BCF topic taslağı hazırlanmalı; teknik sorumlu incelemeli."
    if status == "pending":
        return "Kanıt var ancak sonuç açık değil; manuel teknik kontrol gerekir."
    return "Kayıt izlenebilir; revizyon ve kaynak bağlamı korunmalı."


def compare(clauses: list[dict[str, Any]], evidence: list[dict[str, Any]]) -> dict[str, Any]:
    results = []
    counts = {"passed": 0, "failed": 0, "missing_evidence": 0, "pending": 0, "unknown": 0}
    for clause in clauses:
        matches = [record for record in evidence if matches_clause(clause, record)]
        statuses = [normalize_status(record.get("status") or record.get("result") or record.get("conformance")) for record in matches]
        if not matches:
            status = "missing_evidence"
        elif "failed" in statuses:
            status = "failed"
        elif "passed" in statuses:
            status = "passed"
        elif "pending" in statuses:
            status = "pending"
        else:
            status = "unknown"
        counts[status] += 1
        results.append(
            {
                "clause_id": clause.get("id"),
                "category": clause.get("category"),
                "status": status,
                "required_evidence": clause.get("evidence_required", []),
                "matched_evidence": [
                    {
                        "id": record.get("id") or record.get("file") or record.get("title"),
                        "status": normalize_status(record.get("status") or record.get("result") or record.get("conformance")),
                    }
                    for record in matches
                ],
                "action": action_for(clause, status),
                "clause_text": clause.get("text"),
            }
        )
    return {
        "summary": {
            "total_clauses": len(clauses),
            **counts,
        },
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checklist", required=True, help="extract_spec_clauses.py JSON çıktısı veya CSV liste")
    parser.add_argument("--evidence", help="JSON/CSV/TXT/MD kanıt listesi veya kanıt klasörü")
    parser.add_argument("--output", help="JSON çıktı dosyası")
    args = parser.parse_args()

    clauses = load_clauses(Path(args.checklist))
    evidence = load_evidence(Path(args.evidence) if args.evidence else None)
    payload = compare(clauses, evidence)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
