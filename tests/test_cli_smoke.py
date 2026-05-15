from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_json(*args: str) -> dict:
    result = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    return json.loads(result.stdout)


def flags(items: list[dict], id_key: str, item_id: str) -> set[str]:
    return {item["flag"] for item in items if item[id_key] == item_id}


def test_risk_register_scoring_smoke() -> None:
    payload = run_json(
        "risk-guvenlik-ve-uygunluk-denetimi/scripts/score_risk_register.py",
        str(FIXTURES / "risk_register.json"),
        "--today",
        "2026-05-15",
        "--format",
        "json",
    )

    assert payload["summary"]["risk_count"] == 2
    assert payload["summary"]["high_count"] == 1
    assert payload["summary"]["low_count"] == 1
    assert {"critical_or_high", "missing_evidence_for_high", "overdue"} <= flags(payload["issues"], "risk_id", "R-001")


def test_compliance_checklist_audit_smoke() -> None:
    payload = run_json(
        "risk-guvenlik-ve-uygunluk-denetimi/scripts/audit_compliance_checklist.py",
        str(FIXTURES / "compliance_checklist.json"),
        "--evidence",
        str(FIXTURES / "compliance_evidence.json"),
        "--today",
        "2026-05-15",
        "--format",
        "json",
    )

    assert payload["summary"]["requirement_count"] == 3
    assert payload["summary"]["pass_count"] == 2
    assert payload["summary"]["missing_evidence_count"] == 1
    assert {"mandatory_missing_evidence", "overdue"} <= flags(payload["issues"], "requirement_id", "HSE-001")


def test_communication_pack_validation_smoke() -> None:
    payload = run_json(
        "musteri-ve-taseron-iletisim-hazirlayici/scripts/validate_communication_pack.py",
        str(FIXTURES / "communication_pack.json"),
        "--format",
        "json",
    )

    assert payload["summary"]["message_count"] == 2
    assert payload["summary"]["ready_count"] == 1
    assert payload["summary"]["needs_review_count"] == 1
    assert payload["summary"]["approval_required_count"] == 1
    assert {"financial_risk", "delay_risk", "missing_due_date", "approval_required"} <= flags(
        payload["issues"], "message_id", "MSG-002"
    )


def test_markdown_document_validation_smoke() -> None:
    payload = run_json(
        "dokuman-standartlastirma-ve-formatlama/scripts/validate_markdown_document.py",
        str(FIXTURES / "markdown_with_issues.md"),
        "--required-section",
        "Scope",
        "--required-section",
        "Revision",
        "--format",
        "json",
    )

    issue_flags = {item["flag"] for item in payload["issues"]}
    assert payload["summary"]["status"] == "needs_review"
    assert {"heading_level_skip", "placeholder", "missing_required_section"} <= issue_flags


def test_cost_table_builder_smoke() -> None:
    payload = run_json(
        "teklif-ve-maliyet-tablolama/scripts/build_cost_table.py",
        str(FIXTURES / "cost_items.json"),
        "--format",
        "json",
    )

    assert payload["metadata"]["project"] == "Demo Tower"
    assert payload["summary"]["direct_total"] == 26250.0
    assert payload["summary"]["grand_total"] == 36225.0
    assert payload["qa_flags"] == []


def test_progress_payment_calculator_smoke() -> None:
    payload = run_json(
        "hakedis-ve-mutabakat-kontrolu/scripts/calculate_progress_payment.py",
        str(FIXTURES / "progress_payment.json"),
        "--format",
        "json",
    )

    assert payload["metadata"]["project"] == "Demo Tower"
    assert payload["summary"]["current_gross"] == 27500.0
    assert payload["summary"]["payable_current"] == 31350.0
    assert payload["qa_flags"] == []
