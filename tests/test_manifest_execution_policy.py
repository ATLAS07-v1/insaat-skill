from __future__ import annotations

import importlib.util
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


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_skill_manifest", ROOT / "scripts" / "validate_skill_manifest.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def test_cross_execution_policy_rules_are_enforced_by_manifest_data() -> None:
    index = json.loads((ROOT / "skill-index.json").read_text(encoding="utf-8-sig"))

    for item in index["skills"]:
        manifest = load_manifest(item["name"])
        guardrails = " ".join(manifest["guardrails"]).lower()
        if manifest["risk_level"] == "high":
            assert manifest["requires_human_approval"] is True
        if manifest["execution_mode"] in {"generates_script", "external_application", "file_conversion"}:
            assert manifest["sandbox_required"] is True
        if manifest["network_access"] != "none":
            assert any(token in guardrails for token in ["network", "internet", "url", "api", "kaynak"])


def test_validator_reports_cross_policy_violations() -> None:
    validator = load_validator_module()
    skill_names = {path.name for path in ROOT.iterdir() if path.is_dir() and (path / "SKILL.md").exists()}

    high_risk = load_manifest("teklif-ve-maliyet-tablolama")
    high_risk["requires_human_approval"] = False
    sandboxed = load_manifest("blender-3d-modelleme-ve-render")
    sandboxed["sandbox_required"] = False
    networked = load_manifest("tedarik-ve-malzeme-karsilastirma")
    networked["guardrails"] = ["Sadece genel kalite kontrol yap."]

    cases = [
        ("teklif-ve-maliyet-tablolama", high_risk, "high_risk_requires_human_approval"),
        ("blender-3d-modelleme-ve-render", sandboxed, "execution_mode_requires_sandbox"),
        ("tedarik-ve-malzeme-karsilastirma", networked, "network_access_requires_guardrail"),
    ]
    for skill_name, manifest, expected_flag in cases:
        issues: list[dict] = []
        validator.validate_manifest(skill_name, manifest, skill_names, issues)
        assert expected_flag in {item["flag"] for item in issues}


def test_release_safety_docs_are_present() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    install = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
    limitations = (ROOT / "KNOWN_LIMITATIONS.md").read_text(encoding="utf-8")

    assert "sandbox_required: true" in readme
    assert "sandbox_required" in install
    assert "v0.1.1 Kapsam Dışı Alanlar" in limitations
