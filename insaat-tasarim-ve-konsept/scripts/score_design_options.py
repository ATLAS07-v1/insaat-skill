#!/usr/bin/env python3
"""Score construction design options with weighted concept criteria."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


DEFAULT_WEIGHTS = {
    "program_fit": 0.3,
    "site_response": 0.2,
    "daylight_potential": 0.2,
    "cost_simplicity": 0.2,
    "flexibility": 0.1,
}


def load_options(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict) and isinstance(data.get("options"), list):
            return data["options"]
        if isinstance(data, list):
            return data
        raise SystemExit("JSON içinde `options` listesi veya doğrudan liste beklenir.")
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    raise SystemExit("Desteklenen giriş türleri: .json, .csv")


def load_weights(path: Path | None) -> dict[str, float]:
    if path is None:
        return DEFAULT_WEIGHTS
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    weights = {key: float(value) for key, value in data.items()}
    total = sum(weights.values()) or 1.0
    return {key: value / total for key, value in weights.items()}


def option_score(option: dict[str, Any], weights: dict[str, float]) -> tuple[float, dict[str, float]]:
    scores = option.get("criteria_scores") if isinstance(option.get("criteria_scores"), dict) else option
    normalized_scores: dict[str, float] = {}
    weighted = 0.0
    for key, weight in weights.items():
        try:
            value = float(scores.get(key, 0))
        except (TypeError, ValueError):
            value = 0.0
        normalized_scores[key] = round(value, 2)
        weighted += value * weight
    return round(weighted, 2), normalized_scores


def score(options: list[dict[str, Any]], weights: dict[str, float]) -> dict[str, Any]:
    ranking = []
    for option in options:
        total, scores = option_score(option, weights)
        flags = option.get("flags", [])
        note = "İlk modelleme için güçlü aday."
        if "zoning_not_verified" in flags:
            note = "İmar doğrulaması öncesi sadece konsept adaydır."
        if "high_site_coverage" in flags:
            note = "Kaplama yüksek; açık alan ve çekme mesafesi kontrol edilmeli."
        ranking.append(
            {
                "id": option.get("id"),
                "name": option.get("name"),
                "score": total,
                "criteria_scores": scores,
                "flags": flags,
                "decision_note": note,
            }
        )
    ranking.sort(key=lambda item: item["score"], reverse=True)
    return {"weights": weights, "ranking": ranking}


def to_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Tasarım Karar Matrisi",
        "",
        "| Sıra | ID | Alternatif | Skor | Not |",
        "|---|---|---|---:|---|",
    ]
    for index, item in enumerate(payload["ranking"], start=1):
        lines.append(f"| {index} | {item['id']} | {item['name']} | {item['score']} | {item['decision_note']} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("options", help="Alternatif JSON/CSV dosyası")
    parser.add_argument("--weights", help="Ağırlık JSON dosyası")
    parser.add_argument("--output", help="Çıktı dosyası")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    payload = score(load_options(Path(args.options)), load_weights(Path(args.weights) if args.weights else None))
    rendered = to_markdown(payload) if args.format == "markdown" else json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
