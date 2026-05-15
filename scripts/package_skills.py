#!/usr/bin/env python3
"""Build a portable archive for the construction skill set."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NAME = "insaat-skill-seti"
ROOT_FILES = [
    "README.md",
    "INSTALL.md",
    "DEPENDENCIES.md",
    "requirements.txt",
    "pyproject.toml",
    "manifest.schema.json",
    "skill-index.json",
]
ROOT_DIRS = ["scripts"]
EXAMPLE_DIR = "examples"
IGNORE_PATTERNS = [
    ".git",
    ".github",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "build",
    "dist",
    "*.egg-info",
    "tests",
]


def utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")


def load_index(source_root: Path) -> dict[str, Any]:
    path = source_root / "skill-index.json"
    if not path.exists():
        raise SystemExit(f"skill-index.json not found: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def skill_items(index: dict[str, Any], selected: list[str]) -> list[dict[str, Any]]:
    skills = index.get("skills", [])
    by_name = {item.get("name"): item for item in skills if isinstance(item, dict)}
    if not selected:
        return [item for item in skills if isinstance(item, dict)]
    unknown = sorted(set(selected) - set(by_name))
    if unknown:
        raise SystemExit(f"Unknown skill(s): {', '.join(unknown)}")
    return [by_name[name] for name in selected]


def ensure_empty_dir(path: Path, force: bool) -> None:
    if path.exists():
        if not force:
            raise SystemExit(f"Output already exists. Use --force to replace: {path}")
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_tree(source: Path, target: Path) -> None:
    shutil.copytree(source, target, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))


def copy_root_files(source_root: Path, package_root: Path) -> list[str]:
    copied: list[str] = []
    for name in ROOT_FILES:
        source = source_root / name
        if source.exists():
            shutil.copy2(source, package_root / name)
            copied.append(name)
    return copied


def copy_root_dirs(source_root: Path, package_root: Path) -> list[str]:
    copied: list[str] = []
    for name in ROOT_DIRS:
        source = source_root / name
        if source.exists():
            copy_tree(source, package_root / name)
            copied.append(name)
    return copied


def maybe_copy_examples(source_root: Path, package_root: Path, args: argparse.Namespace) -> bool:
    source = source_root / EXAMPLE_DIR
    if args.no_examples or not source.exists():
        return False
    if args.skill and not args.include_examples:
        return False
    copy_tree(source, package_root / EXAMPLE_DIR)
    return True


def filter_related_skills(package_root: Path, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected_names = {item["name"] for item in items}
    filtered_items = copy.deepcopy(items)
    for item in filtered_items:
        item["related_skills"] = [name for name in item.get("related_skills", []) if name in selected_names]
        manifest_path = package_root / item["name"] / "agents" / "openai.yaml"
        if manifest_path.exists():
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8-sig"))
            if isinstance(manifest, dict):
                manifest["related_skills"] = [name for name in manifest.get("related_skills", []) if name in selected_names]
                manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
    return filtered_items


def write_filtered_index(source_index: dict[str, Any], package_root: Path, items: list[dict[str, Any]]) -> None:
    filtered_index = copy.deepcopy(source_index)
    filtered_index["generated_at"] = utc_now()
    filtered_index["skill_count"] = len(items)
    filtered_index["skills"] = items
    (package_root / "skill-index.json").write_text(
        json.dumps(filtered_index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_zip(package_root: Path, archive_path: Path) -> None:
    if archive_path.exists():
        archive_path.unlink()
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(package_root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(package_root.parent).as_posix())


def render_markdown(payload: dict[str, Any]) -> str:
    lines = ["# Skill Paketleme Sonucu", ""]
    lines.append(f"- Durum: {payload['status']}")
    lines.append(f"- Paket klasoru: {payload['package_dir']}")
    lines.append(f"- Skill sayisi: {payload['skill_count']}")
    if payload.get("archive"):
        lines.append(f"- Arsiv: {payload['archive']['path']}")
        lines.append(f"- SHA256: {payload['archive']['sha256']}")
    return "\n".join(lines)


def build_package(args: argparse.Namespace) -> dict[str, Any]:
    source_root = Path(args.source_root).resolve()
    index = load_index(source_root)
    selected_items = skill_items(index, args.skill or [])
    output_dir = Path(args.output_dir).resolve()
    package_root = output_dir / args.name

    ensure_empty_dir(package_root, args.force)
    copied_files = copy_root_files(source_root, package_root)
    copied_dirs = copy_root_dirs(source_root, package_root)
    examples_copied = maybe_copy_examples(source_root, package_root, args)
    if examples_copied:
        copied_dirs.append(EXAMPLE_DIR)

    copied_skills: list[dict[str, Any]] = []
    for item in selected_items:
        name = item["name"]
        source = source_root / name
        if not source.exists():
            raise SystemExit(f"Skill folder not found: {source}")
        copy_tree(source, package_root / name)
        copied_skills.append(
            {
                "name": name,
                "path": name,
                "manifest": f"{name}/agents/openai.yaml",
                "entrypoint": f"{name}/SKILL.md",
                "dependency_groups": item.get("dependency_groups", []),
                "system_tools": item.get("system_tools", []),
                "risk_level": item.get("risk_level", ""),
                "requires_human_approval": item.get("requires_human_approval", False),
                "related_skills": [related for related in item.get("related_skills", []) if related in {entry["name"] for entry in selected_items}],
            }
        )

    filtered_items = filter_related_skills(package_root, selected_items)
    write_filtered_index(index, package_root, filtered_items)

    package_manifest = {
        "name": args.name,
        "source_name": index.get("name"),
        "version": index.get("version"),
        "schema_version": index.get("schema_version"),
        "source_repository": index.get("repository"),
        "generated_at": utc_now(),
        "skill_count": len(copied_skills),
        "skills": copied_skills,
        "root_files": copied_files,
        "root_dirs": copied_dirs,
    }
    (package_root / "package-manifest.json").write_text(
        json.dumps(package_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    archive_payload: dict[str, Any] | None = None
    if not args.no_zip:
        output_dir.mkdir(parents=True, exist_ok=True)
        archive_path = output_dir / f"{args.name}.zip"
        create_zip(package_root, archive_path)
        archive_payload = {
            "path": str(archive_path),
            "sha256": file_sha256(archive_path),
            "size_bytes": archive_path.stat().st_size,
        }

    return {
        "status": "ok",
        "package_dir": str(package_root),
        "package_manifest": str(package_root / "package-manifest.json"),
        "skill_count": len(copied_skills),
        "skills": [item["name"] for item in copied_skills],
        "archive": archive_payload,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", default=str(ROOT), help="Repository or package root containing skill-index.json.")
    parser.add_argument("--output-dir", default=str(ROOT / "dist"), help="Directory where the package folder is created.")
    parser.add_argument("--name", default=DEFAULT_NAME, help="Package folder and archive name.")
    parser.add_argument("--skill", action="append", help="Skill name to include. Repeat for multiple skills. Defaults to all.")
    parser.add_argument("--include-examples", action="store_true", help="Include examples even when packaging a skill subset.")
    parser.add_argument("--no-examples", action="store_true", help="Skip example files.")
    parser.add_argument("--no-zip", action="store_true", help="Create only the package folder.")
    parser.add_argument("--force", action="store_true", help="Replace an existing output package folder.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    payload = build_package(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
