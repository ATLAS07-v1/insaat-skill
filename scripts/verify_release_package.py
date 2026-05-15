#!/usr/bin/env python3
"""Extract and validate a release ZIP from inside the packaged directory."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any


DEFAULT_PACKAGE_NAME = "insaat-skill-seti"
REQUIRED_PACKAGE_PATHS = [
    "skill-index.json",
    "manifest.schema.json",
    "package-manifest.json",
    "scripts/validate_skill_manifest.py",
    "scripts/run_examples.py",
    "schemas/handoff-envelope.schema.json",
    "examples/quickstart/inputs/risk_register.json",
]


def ensure_empty_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def safe_extract(archive_path: Path, output_dir: Path) -> None:
    root = output_dir.resolve()
    with zipfile.ZipFile(archive_path) as zipped:
        for member in zipped.infolist():
            target = (output_dir / member.filename).resolve()
            try:
                target.relative_to(root)
            except ValueError as exc:
                raise SystemExit(f"Unsafe zip member path: {member.filename}") from exc
        zipped.extractall(output_dir)


def run_json(package_root: Path, *args: str) -> tuple[dict[str, Any], int, str]:
    result = subprocess.run(
        [sys.executable, *args],
        cwd=package_root,
        text=True,
        capture_output=True,
        check=False,
    )
    combined = result.stdout + result.stderr
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        payload = {}
    return payload, result.returncode, combined


def check_required_paths(package_root: Path) -> list[str]:
    return [path for path in REQUIRED_PACKAGE_PATHS if not (package_root / path).exists()]


def verify_package(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    archive_path = Path(args.archive).resolve()
    if not archive_path.exists():
        raise SystemExit(f"Archive not found: {archive_path}")

    work_dir = Path(args.work_dir).resolve()
    ensure_empty_dir(work_dir)
    safe_extract(archive_path, work_dir)
    package_root = work_dir / args.package_name
    if not package_root.exists():
        raise SystemExit(f"Package root not found after extract: {package_root}")

    missing_paths = check_required_paths(package_root)
    index = json.loads((package_root / "skill-index.json").read_text(encoding="utf-8-sig"))

    manifest_payload, manifest_status, manifest_output = run_json(
        package_root,
        "scripts/validate_skill_manifest.py",
        "--format",
        "json",
    )
    example_payload, example_status, example_output = run_json(
        package_root,
        "scripts/run_examples.py",
        "--scenario",
        "quickstart",
        "--output-dir",
        str(work_dir / "quickstart-output"),
        "--format",
        "json",
    )

    issues: list[dict[str, str]] = []
    for path in missing_paths:
        issues.append({"flag": "missing_required_path", "message": path})
    if index.get("skill_count") != 17:
        issues.append({"flag": "invalid_skill_count", "message": f"skill_count={index.get('skill_count')}"})
    if manifest_status != 0 or manifest_payload.get("summary", {}).get("status") != "pass":
        issues.append({"flag": "manifest_validation_failed", "message": manifest_output[-1000:]})
    if example_status != 0 or example_payload.get("status") != "ok":
        issues.append({"flag": "quickstart_failed", "message": example_output[-1000:]})

    payload = {
        "status": "ok" if not issues else "fail",
        "archive": str(archive_path),
        "package_root": str(package_root),
        "skill_count": index.get("skill_count"),
        "required_paths_checked": len(REQUIRED_PACKAGE_PATHS),
        "manifest_status": manifest_payload.get("summary", {}).get("status"),
        "quickstart_status": example_payload.get("status"),
        "issues": issues,
    }
    return payload, 0 if not issues else 1


def render_markdown(payload: dict[str, Any]) -> str:
    lines = ["# Release Package Verification", ""]
    lines.append(f"- Status: {payload['status']}")
    lines.append(f"- Archive: {payload['archive']}")
    lines.append(f"- Package root: {payload['package_root']}")
    lines.append(f"- Skill count: {payload['skill_count']}")
    lines.append(f"- Manifest validation: {payload['manifest_status']}")
    lines.append(f"- Quickstart: {payload['quickstart_status']}")
    if payload["issues"]:
        lines.extend(["", "## Issues", ""])
        for item in payload["issues"]:
            lines.append(f"- {item['flag']}: {item['message']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", help="Release ZIP path.")
    parser.add_argument("--work-dir", default="dist/release-verify", help="Temporary extraction and validation directory.")
    parser.add_argument("--package-name", default=DEFAULT_PACKAGE_NAME, help="Top-level package folder name inside the ZIP.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    payload, status = verify_package(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
