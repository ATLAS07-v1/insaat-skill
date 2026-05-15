from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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


def test_skill_manifests_pass_repository_validator() -> None:
    payload = run_json("scripts/validate_skill_manifest.py", "--format", "json")

    assert payload["summary"] == {
        "skill_count": 17,
        "manifest_count": 17,
        "issue_count": 0,
        "status": "pass",
    }
    assert payload["issues"] == []
