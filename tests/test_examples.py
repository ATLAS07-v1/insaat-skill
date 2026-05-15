from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_quickstart_examples_run_end_to_end(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_examples.py",
            "--scenario",
            "quickstart",
            "--output-dir",
            str(tmp_path),
            "--format",
            "json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    summaries = {step["id"]: step["summary"] for step in payload["steps"]}

    assert payload["status"] == "ok"
    assert payload["step_count"] == 6
    assert summaries["risk_score"]["risk_count"] == 2
    assert summaries["compliance_audit"]["missing_evidence_count"] == 1
    assert summaries["communication_check"]["needs_review_count"] == 1
    assert summaries["document_markdown_qa"]["status"] == "needs_review"
    assert summaries["cost_table"]["grand_total"] == 36225.0
    assert summaries["progress_payment"]["payable_current"] == 31350.0
    assert (tmp_path / "summary.json").exists()
