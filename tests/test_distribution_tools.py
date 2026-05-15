from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_json(*args: str, expect_success: bool = True) -> tuple[dict, int]:
    result = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if expect_success:
        assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    return payload, result.returncode


def test_package_skills_builds_portable_subset(tmp_path: Path) -> None:
    payload, status = run_json(
        "scripts/package_skills.py",
        "--output-dir",
        str(tmp_path),
        "--name",
        "demo-package",
        "--skill",
        "insaat-arac-kullanimlari",
        "--skill",
        "dokuman-standartlastirma-ve-formatlama",
        "--force",
        "--format",
        "json",
    )

    package_dir = Path(payload["package_dir"])
    archive = Path(payload["archive"]["path"])
    manifest = json.loads((package_dir / "package-manifest.json").read_text(encoding="utf-8"))
    index = json.loads((package_dir / "skill-index.json").read_text(encoding="utf-8"))

    assert status == 0
    assert payload["status"] == "ok"
    assert payload["skill_count"] == 2
    assert (package_dir / "skill-index.json").exists()
    assert (package_dir / "LICENSE").exists()
    assert (package_dir / "scripts" / "install_skills.py").exists()
    assert (package_dir / "schemas" / "risk-register.schema.json").exists()
    assert (package_dir / "schemas" / "handoff-envelope.schema.json").exists()
    assert not (package_dir / "examples").exists()
    assert (package_dir / "insaat-arac-kullanimlari" / "SKILL.md").exists()
    assert (package_dir / "dokuman-standartlastirma-ve-formatlama" / "agents" / "openai.yaml").exists()
    assert manifest["skill_count"] == 2
    assert index["skill_count"] == 2
    assert {item["name"] for item in index["skills"]} == {"insaat-arac-kullanimlari", "dokuman-standartlastirma-ve-formatlama"}
    assert len(payload["archive"]["sha256"]) == 64

    validation_payload, validation_status = run_json(
        str(package_dir / "scripts" / "validate_skill_manifest.py"),
        "--format",
        "json",
    )
    assert validation_status == 0
    assert validation_payload["summary"]["status"] == "pass"

    with zipfile.ZipFile(archive) as zipped:
        names = set(zipped.namelist())
    assert "demo-package/package-manifest.json" in names
    assert "demo-package/insaat-arac-kullanimlari/SKILL.md" in names


def test_install_skills_copies_selected_skill_from_package(tmp_path: Path) -> None:
    package_payload, _ = run_json(
        "scripts/package_skills.py",
        "--output-dir",
        str(tmp_path),
        "--name",
        "installable-package",
        "--skill",
        "risk-guvenlik-ve-uygunluk-denetimi",
        "--force",
        "--no-zip",
        "--format",
        "json",
    )
    package_dir = Path(package_payload["package_dir"])
    target_dir = tmp_path / "agent-skills"

    dry_payload, dry_status = run_json(
        "scripts/install_skills.py",
        "--source-root",
        str(package_dir),
        "--target",
        str(target_dir),
        "--skill",
        "risk-guvenlik-ve-uygunluk-denetimi",
        "--dry-run",
        "--format",
        "json",
    )

    assert dry_status == 0
    assert dry_payload["actions"][0]["status"] == "would_copy"
    assert not target_dir.exists()

    install_payload, install_status = run_json(
        "scripts/install_skills.py",
        "--source-root",
        str(package_dir),
        "--target",
        str(target_dir),
        "--skill",
        "risk-guvenlik-ve-uygunluk-denetimi",
        "--format",
        "json",
    )

    installed_skill = target_dir / "risk-guvenlik-ve-uygunluk-denetimi"
    assert install_status == 0
    assert install_payload["copied_count"] == 1
    assert (installed_skill / "SKILL.md").exists()
    assert (installed_skill / "agents" / "openai.yaml").exists()


def test_full_package_includes_quickstart_examples(tmp_path: Path) -> None:
    payload, status = run_json(
        "scripts/package_skills.py",
        "--output-dir",
        str(tmp_path),
        "--name",
        "full-package",
        "--force",
        "--no-zip",
        "--format",
        "json",
    )

    package_dir = Path(payload["package_dir"])
    example_input = package_dir / "examples" / "quickstart" / "inputs" / "risk_register.json"

    assert status == 0
    assert payload["skill_count"] == 17
    assert example_input.exists()


def test_install_skills_blocks_existing_target_without_force(tmp_path: Path) -> None:
    target_dir = tmp_path / "agent-skills"
    skill_dir = target_dir / "insaat-arac-kullanimlari"
    skill_dir.mkdir(parents=True)

    payload, status = run_json(
        "scripts/install_skills.py",
        "--target",
        str(target_dir),
        "--skill",
        "insaat-arac-kullanimlari",
        "--format",
        "json",
        expect_success=False,
    )

    assert status == 1
    assert payload["status"] == "blocked"
    assert payload["actions"][0]["reason"] == "target_exists"
