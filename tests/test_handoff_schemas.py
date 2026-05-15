from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def test_handoff_schemas_are_valid_json_schema_documents() -> None:
    schemas = sorted((ROOT / "schemas").glob("*.schema.json"))

    assert len(schemas) >= 6
    for path in schemas:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_handoff_schema_examples_validate() -> None:
    examples = {
        "risk-register.schema.json": {"risks": [{"id": "R-001", "hazard": "Fall", "likelihood": 4, "severity": 5}]},
        "evidence-register.schema.json": {"evidence": [{"id": "EV-001", "file": "photo.jpg"}]},
        "quantity-handoff.schema.json": {"items": [{"code": "Q-001", "quantity": 12.5, "unit": "m3"}]},
        "cost-table-input.schema.json": {"items": [{"code": "C-001", "quantity": 1.0, "unit_price": 100.0, "unit": "m3"}]},
        "communication-pack.schema.json": {
            "messages": [{"project": "Demo", "subject": "RFI", "recipient": "Client", "request": "Please review."}]
        },
        "document-manifest.schema.json": {"documents": [{"path": "report.pdf"}]},
    }

    for file_name, payload in examples.items():
        schema = json.loads((ROOT / "schemas" / file_name).read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(payload)
