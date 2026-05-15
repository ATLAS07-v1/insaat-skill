from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_release_artifact_builder_outputs_checksum_metadata_and_notes(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_release_artifacts.py",
            "--version",
            "v0.1.0",
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
    archive = Path(payload["archive"]["path"])
    metadata = json.loads(Path(payload["metadata"]).read_text(encoding="utf-8"))
    checksum_line = (tmp_path / "SHA256SUMS.txt").read_text(encoding="utf-8").strip()
    notes = (tmp_path / "release-notes.md").read_text(encoding="utf-8")

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    assert payload["tag"] == "v0.1.0"
    assert payload["skill_count"] == 17
    assert archive.exists()
    assert checksum_line == f"{digest}  {archive.name}"
    assert metadata["archive"]["sha256"] == digest
    assert "İnşaat Skill Seti v0.1.0" in notes


def test_release_workflow_uses_current_official_actions_and_release_artifacts() -> None:
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")

    assert "actions/checkout@v6" in workflow
    assert "actions/setup-python@v6" in workflow
    assert "actions/upload-artifact@v7" in workflow
    assert "python scripts/build_release_artifacts.py" in workflow
    assert "gh release create" in workflow
    assert "dist/release/insaat-skill-seti.zip" in workflow
