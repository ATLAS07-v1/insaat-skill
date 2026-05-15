from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SANDBOX_REQUIRED_SKILLS = {
    "cad-autocad-dwg-dxf-isleme",
    "bim-revit-ifc-model-kontrolu",
    "blender-3d-modelleme-ve-render",
    "sketchup-konsept-ve-kutle-modelleme",
    "cizim-dosya-donusum-ve-qa",
    "metraj-ve-mahal-kontrolu",
    "saha-fotograf-ve-kanit-analizi",
    "dokuman-standartlastirma-ve-formatlama",
}
EXECUTION_FIELDS = {
    "sandbox_required",
    "execution_mode",
    "max_runtime_seconds",
    "network_access",
    "writes_files",
    "resource_limits",
}


def load_manifest(skill_name: str) -> dict:
    return yaml.safe_load((ROOT / skill_name / "agents" / "openai.yaml").read_text(encoding="utf-8-sig"))


def test_execution_policy_fields_exist_for_every_skill() -> None:
    index = json.loads((ROOT / "skill-index.json").read_text(encoding="utf-8-sig"))

    for item in index["skills"]:
        manifest = load_manifest(item["name"])
        assert EXECUTION_FIELDS <= set(item)
        assert EXECUTION_FIELDS <= set(manifest)
        assert item["sandbox_required"] == manifest["sandbox_required"]
        assert item["execution_mode"] == manifest["execution_mode"]
        assert item["resource_limits"] == manifest["resource_limits"]
        assert manifest["max_runtime_seconds"] > 0
        assert manifest["network_access"] in {"none", "optional", "required"}


def test_risky_external_tool_skills_require_sandbox() -> None:
    for skill_name in SANDBOX_REQUIRED_SKILLS:
        manifest = load_manifest(skill_name)
        assert manifest["sandbox_required"] is True
        assert manifest["max_runtime_seconds"] >= 300


def test_release_safety_docs_are_present() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    install = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
    limitations = (ROOT / "KNOWN_LIMITATIONS.md").read_text(encoding="utf-8")

    assert "sandbox_required: true" in readme
    assert "sandbox_required" in install
    assert "v0.1.0 Kapsam Dışı Alanlar" in limitations
