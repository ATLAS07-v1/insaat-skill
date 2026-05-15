from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_system_tool_check_reports_core_and_optional_tools() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_system_tools.py", "--skill", "cad-autocad-dwg-dxf-isleme", "--format", "json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["summary"]["skill_count"] == 1
    assert "core" in payload["dependency_groups"]
    assert "cad" in payload["dependency_groups"]
    assert any(item["module"] == "yaml" and item["status"] == "available" for item in payload["python_modules"])
    assert any(item["tool"] == "ODA File Converter" for item in payload["system_tools"])


def test_system_tool_check_markdown_output() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_system_tools.py", "--skill", "insaat-hesaplamalar", "--format", "markdown"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    assert "# System Tool Check" in result.stdout
    assert "Python Modules" in result.stdout
