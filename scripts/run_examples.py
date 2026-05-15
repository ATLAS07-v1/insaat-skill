#!/usr/bin/env python3
"""Run deterministic quickstart examples and write JSON outputs."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

SCENARIOS: dict[str, list[dict[str, Any]]] = {
    "quickstart": [
        {
            "id": "risk_score",
            "script": "risk-guvenlik-ve-uygunluk-denetimi/scripts/score_risk_register.py",
            "args": ["risk_register.json", "--today", "2026-05-15", "--format", "json"],
            "output": "risk_score.json",
        },
        {
            "id": "compliance_audit",
            "script": "risk-guvenlik-ve-uygunluk-denetimi/scripts/audit_compliance_checklist.py",
            "args": [
                "compliance_checklist.json",
                "--evidence",
                "compliance_evidence.json",
                "--today",
                "2026-05-15",
                "--format",
                "json",
            ],
            "output": "compliance_audit.json",
        },
        {
            "id": "communication_check",
            "script": "musteri-ve-taseron-iletisim-hazirlayici/scripts/validate_communication_pack.py",
            "args": ["communication_pack.json", "--format", "json"],
            "output": "communication_check.json",
        },
        {
            "id": "document_markdown_qa",
            "script": "dokuman-standartlastirma-ve-formatlama/scripts/validate_markdown_document.py",
            "args": ["site_report_with_issues.md", "--required-section", "Scope", "--required-section", "Revision", "--format", "json"],
            "output": "document_markdown_qa.json",
        },
        {
            "id": "cost_table",
            "script": "teklif-ve-maliyet-tablolama/scripts/build_cost_table.py",
            "args": ["cost_items.json", "--format", "json"],
            "output": "cost_table.json",
        },
        {
            "id": "progress_payment",
            "script": "hakedis-ve-mutabakat-kontrolu/scripts/calculate_progress_payment.py",
            "args": ["progress_payment.json", "--format", "json"],
            "output": "progress_payment.json",
        },
    ]
}


def scenario_input_dir(name: str) -> Path:
    return ROOT / "examples" / name / "inputs"


def resolve_args(raw_args: list[str], input_dir: Path) -> list[str]:
    resolved: list[str] = []
    for item in raw_args:
        candidate = input_dir / item
        resolved.append(str(candidate) if candidate.exists() else item)
    return resolved


def step_summary(payload: dict[str, Any]) -> dict[str, Any]:
    summary = payload.get("summary")
    if isinstance(summary, dict):
        return summary
    return {}


def run_step(step: dict[str, Any], input_dir: Path, output_dir: Path) -> dict[str, Any]:
    script = ROOT / step["script"]
    if not script.exists():
        raise SystemExit(f"Script not found for example step {step['id']}: {script}")
    output_path = output_dir / step["output"]
    command = [sys.executable, str(script), *resolve_args(step["args"], input_dir), "--output", str(output_path)]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        return {
            "id": step["id"],
            "status": "failed",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output": str(output_path),
        }
    payload = json.loads(output_path.read_text(encoding="utf-8-sig"))
    return {
        "id": step["id"],
        "status": "ok",
        "output": str(output_path),
        "summary": step_summary(payload),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = ["# Example Run Summary", ""]
    lines.append(f"- Scenario: {payload['scenario']}")
    lines.append(f"- Status: {payload['status']}")
    lines.append(f"- Output dir: {payload['output_dir']}")
    lines.extend(["", "## Steps", ""])
    for step in payload["steps"]:
        lines.append(f"- {step['id']}: {step['status']}")
    return "\n".join(lines)


def run_scenario(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    if args.scenario not in SCENARIOS:
        raise SystemExit(f"Unknown scenario: {args.scenario}")
    input_dir = scenario_input_dir(args.scenario)
    if not input_dir.exists():
        raise SystemExit(f"Example input directory not found: {input_dir}")
    output_dir = Path(args.output_dir).resolve() if args.output_dir else ROOT / "dist" / "example-runs" / args.scenario
    output_dir.mkdir(parents=True, exist_ok=True)

    steps = [run_step(step, input_dir, output_dir) for step in SCENARIOS[args.scenario]]
    status = "ok" if all(step["status"] == "ok" for step in steps) else "failed"
    payload = {
        "scenario": args.scenario,
        "status": status,
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "step_count": len(steps),
        "steps": steps,
    }
    (output_dir / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload, 0 if status == "ok" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="quickstart")
    parser.add_argument("--output-dir", help="Directory for generated example outputs. Defaults to dist/example-runs/<scenario>.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    payload, status = run_scenario(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
