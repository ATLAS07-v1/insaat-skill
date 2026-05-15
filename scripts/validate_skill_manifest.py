#!/usr/bin/env python3
"""Validate the root skill index and every agents/openai.yaml manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_MANIFEST_FIELDS = {
    "schema_version",
    "name",
    "version",
    "language",
    "display_name",
    "description",
    "entrypoint",
    "default_prompt",
    "python_requires",
    "dependency_groups",
    "system_tools",
    "tags",
    "triggers",
    "inputs",
    "outputs",
    "guardrails",
    "risk_level",
    "requires_human_approval",
    "human_approval_contexts",
    "sandbox_required",
    "execution_mode",
    "max_runtime_seconds",
    "network_access",
    "writes_files",
    "resource_limits",
    "tools",
    "related_skills",
}
REQUIRED_INDEX_FIELDS = {"schema_version", "name", "version", "language", "description", "repository", "skill_count", "skills"}
RISK_LEVELS = {"low", "medium", "high"}
EXECUTION_MODES = {"analysis_only", "local_cli", "file_conversion", "external_application", "generates_script"}
NETWORK_ACCESS = {"none", "optional", "required"}


def issue(issues: list[dict[str, Any]], target: str, flag: str, message: str) -> None:
    issues.append({"target": target, "flag": flag, "message": message})


def load_index(issues: list[dict[str, Any]]) -> dict[str, Any]:
    path = ROOT / "skill-index.json"
    if not path.exists():
        issue(issues, "skill-index.json", "missing_file", "skill-index.json bulunamadı.")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        issue(issues, "skill-index.json", "invalid_json", str(exc))
        return {}


def check_schema_file(issues: list[dict[str, Any]]) -> dict[str, Any]:
    path = ROOT / "manifest.schema.json"
    if not path.exists():
        issue(issues, "manifest.schema.json", "missing_file", "manifest.schema.json bulunamadı.")
        return {}
    try:
        schema = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        issue(issues, "manifest.schema.json", "invalid_json", str(exc))
        return {}
    for field in ("$schema", "$defs", "required", "properties"):
        if field not in schema:
            issue(issues, "manifest.schema.json", "missing_schema_field", f"Eksik schema alanı: {field}")
    return schema


def schema_path(error_path: Any) -> str:
    parts = [str(part) for part in error_path]
    return ".".join(parts) if parts else "$"


def validate_with_schema(target: str, payload: dict[str, Any], schema: dict[str, Any], issues: list[dict[str, Any]]) -> None:
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(payload), key=lambda item: list(item.path)):
        issue(issues, target, "schema_validation_error", f"{schema_path(error.path)}: {error.message}")


def skill_manifest_schema(root_schema: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": root_schema.get("$schema", "https://json-schema.org/draft/2020-12/schema"),
        "$defs": root_schema.get("$defs", {}),
        **root_schema.get("$defs", {}).get("skill_manifest", {}),
    }


def load_manifest(skill_name: str, issues: list[dict[str, Any]]) -> dict[str, Any]:
    path = ROOT / skill_name / "agents" / "openai.yaml"
    if not path.exists():
        issue(issues, skill_name, "missing_manifest", "agents/openai.yaml bulunamadı.")
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except yaml.YAMLError as exc:
        issue(issues, skill_name, "invalid_yaml", str(exc))
        return {}
    if not isinstance(data, dict):
        issue(issues, skill_name, "invalid_manifest", "Manifest YAML nesnesi olmalıdır.")
        return {}
    return data


def check_list(value: Any, target: str, field: str, issues: list[dict[str, Any]], min_len: int = 1) -> None:
    if not isinstance(value, list) or len(value) < min_len:
        issue(issues, target, "invalid_list", f"{field} en az {min_len} öğeli liste olmalıdır.")


def validate_manifest(skill_name: str, manifest: dict[str, Any], all_skill_names: set[str], issues: list[dict[str, Any]]) -> None:
    missing = sorted(REQUIRED_MANIFEST_FIELDS - set(manifest))
    for field in missing:
        issue(issues, skill_name, "missing_manifest_field", f"Eksik alan: {field}")
    if not manifest:
        return
    if manifest.get("name") != skill_name:
        issue(issues, skill_name, "name_mismatch", f"Manifest name {manifest.get('name')!r}, klasör adı {skill_name!r}.")
    if not str(manifest.get("python_requires", "")).startswith(">="):
        issue(issues, skill_name, "invalid_python_requires", "python_requires >=x.y biçiminde olmalıdır.")
    entrypoint = ROOT / skill_name / str(manifest.get("entrypoint", ""))
    if not entrypoint.exists():
        issue(issues, skill_name, "missing_entrypoint", f"Entrypoint yok: {manifest.get('entrypoint')}")
    for field in ("dependency_groups", "tags", "triggers", "inputs", "outputs", "guardrails", "human_approval_contexts"):
        check_list(manifest.get(field), skill_name, field, issues)
    check_list(manifest.get("system_tools"), skill_name, "system_tools", issues, min_len=0)
    if not isinstance(manifest.get("sandbox_required"), bool):
        issue(issues, skill_name, "invalid_sandbox_required", "sandbox_required bool olmalıdır.")
    if manifest.get("execution_mode") not in EXECUTION_MODES:
        issue(issues, skill_name, "invalid_execution_mode", "execution_mode geçerli değil.")
    if not isinstance(manifest.get("max_runtime_seconds"), int) or int(manifest.get("max_runtime_seconds", 0)) <= 0:
        issue(issues, skill_name, "invalid_max_runtime_seconds", "max_runtime_seconds pozitif integer olmalıdır.")
    if manifest.get("network_access") not in NETWORK_ACCESS:
        issue(issues, skill_name, "invalid_network_access", "network_access none, optional veya required olmalıdır.")
    if not isinstance(manifest.get("writes_files"), bool):
        issue(issues, skill_name, "invalid_writes_files", "writes_files bool olmalıdır.")
    limits = manifest.get("resource_limits")
    if not isinstance(limits, dict):
        issue(issues, skill_name, "invalid_resource_limits", "resource_limits dict olmalıdır.")
    else:
        for key in ("max_input_size_mb", "max_output_size_mb", "recommended_memory_mb"):
            if not isinstance(limits.get(key), int) or int(limits.get(key, 0)) <= 0:
                issue(issues, skill_name, "invalid_resource_limit", f"resource_limits.{key} pozitif integer olmalıdır.")
    if manifest.get("risk_level") not in RISK_LEVELS:
        issue(issues, skill_name, "invalid_risk_level", "risk_level low, medium veya high olmalıdır.")
    if not isinstance(manifest.get("requires_human_approval"), bool):
        issue(issues, skill_name, "invalid_approval_flag", "requires_human_approval bool olmalıdır.")
    tools = manifest.get("tools")
    check_list(tools, skill_name, "tools", issues, min_len=0)
    if isinstance(tools, list):
        for tool in tools:
            if not isinstance(tool, dict):
                issue(issues, skill_name, "invalid_tool", "tool nesnesi dict olmalıdır.")
                continue
            for key in ("name", "type", "path", "command"):
                if not tool.get(key):
                    issue(issues, skill_name, "missing_tool_field", f"Tool alanı eksik: {key}")
            tool_path = ROOT / skill_name / str(tool.get("path", ""))
            if tool.get("path") and not tool_path.exists():
                issue(issues, skill_name, "missing_tool_path", f"Tool dosyası yok: {tool.get('path')}")
    related = manifest.get("related_skills")
    check_list(related, skill_name, "related_skills", issues, min_len=0)
    if isinstance(related, list):
        for related_skill in related:
            if related_skill not in all_skill_names:
                issue(issues, skill_name, "unknown_related_skill", f"Bilinmeyen related skill: {related_skill}")


def validate_index(index: dict[str, Any], manifests: dict[str, dict[str, Any]], issues: list[dict[str, Any]]) -> None:
    missing = sorted(REQUIRED_INDEX_FIELDS - set(index))
    for field in missing:
        issue(issues, "skill-index.json", "missing_index_field", f"Eksik alan: {field}")
    skills = index.get("skills", [])
    if not isinstance(skills, list):
        issue(issues, "skill-index.json", "invalid_skills", "skills liste olmalıdır.")
        return
    if index.get("skill_count") != len(skills):
        issue(issues, "skill-index.json", "skill_count_mismatch", "skill_count ile skills uzunluğu farklı.")
    names = [item.get("name") for item in skills if isinstance(item, dict)]
    if len(names) != len(set(names)):
        issue(issues, "skill-index.json", "duplicate_skill_name", "Tekrarlı skill adı var.")
    manifest_names = set(manifests)
    if set(names) != manifest_names:
        issue(issues, "skill-index.json", "index_manifest_mismatch", "Index skill listesi ile manifest klasörleri farklı.")
    for item in skills:
        if not isinstance(item, dict):
            issue(issues, "skill-index.json", "invalid_skill_item", "Skill item dict olmalıdır.")
            continue
        name = item.get("name")
        if not name:
            issue(issues, "skill-index.json", "missing_skill_name", "Skill item name içermiyor.")
            continue
        manifest = manifests.get(name, {})
        for field in (
            "version",
            "description",
            "python_requires",
            "dependency_groups",
            "system_tools",
            "tags",
            "triggers",
            "inputs",
            "outputs",
            "tools",
            "risk_level",
            "requires_human_approval",
            "sandbox_required",
            "execution_mode",
            "max_runtime_seconds",
            "network_access",
            "writes_files",
            "resource_limits",
        ):
            if item.get(field) != manifest.get(field):
                issue(issues, name, "index_manifest_field_mismatch", f"Index ve manifest alanı farklı: {field}")
        for path_field in ("path", "manifest", "entrypoint"):
            value = item.get(path_field)
            if not value:
                issue(issues, name, "missing_index_path", f"Index path alanı eksik: {path_field}")
            elif not (ROOT / value).exists():
                issue(issues, name, "missing_index_path_target", f"Index path hedefi yok: {value}")


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = ["# Skill Manifest Doğrulama", ""]
    lines.append(f"- Skill sayısı: {summary['skill_count']}")
    lines.append(f"- Manifest sayısı: {summary['manifest_count']}")
    lines.append(f"- Issue sayısı: {summary['issue_count']}")
    lines.append(f"- Durum: {summary['status']}")
    if payload["issues"]:
        lines.extend(["", "## Bulgular", "", "| Target | Flag | Message |", "|---|---|---|"])
        for item in payload["issues"]:
            lines.append(f"| {item['target']} | {item['flag']} | {item['message']} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    issues: list[dict[str, Any]] = []
    skill_dirs = sorted(path.name for path in ROOT.iterdir() if path.is_dir() and (path / "SKILL.md").exists())
    all_skill_names = set(skill_dirs)
    manifests = {name: load_manifest(name, issues) for name in skill_dirs}
    schema = check_schema_file(issues)
    if schema:
        manifest_schema = skill_manifest_schema(schema)
        for name, manifest in manifests.items():
            if manifest:
                validate_with_schema(name, manifest, manifest_schema, issues)
    for name, manifest in manifests.items():
        validate_manifest(name, manifest, all_skill_names, issues)
    index = load_index(issues)
    if index:
        if schema:
            validate_with_schema("skill-index.json", index, schema, issues)
        validate_index(index, manifests, issues)
    payload = {
        "summary": {
            "skill_count": len(skill_dirs),
            "manifest_count": len([item for item in manifests.values() if item]),
            "issue_count": len(issues),
            "status": "pass" if not issues else "fail",
        },
        "issues": issues,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
