#!/usr/bin/env python3
"""Install selected construction skills into a local agent skill directory."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
IGNORE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
]


def load_index(source_root: Path) -> dict[str, Any]:
    path = source_root / "skill-index.json"
    if not path.exists():
        raise SystemExit(f"skill-index.json not found: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def default_target() -> Path | None:
    hermes_target = os.environ.get("HERMES_SKILLS_DIR")
    if hermes_target:
        return Path(hermes_target)
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return None


def select_skills(index: dict[str, Any], selected: list[str]) -> list[str]:
    names = [item["name"] for item in index.get("skills", []) if isinstance(item, dict) and item.get("name")]
    if not selected:
        return names
    unknown = sorted(set(selected) - set(names))
    if unknown:
        raise SystemExit(f"Unknown skill(s): {', '.join(unknown)}")
    return selected


def is_inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def install(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    source_root = Path(args.source_root).resolve()
    index = load_index(source_root)
    skills = select_skills(index, args.skill or [])
    target_root = Path(args.target).resolve() if args.target else default_target()
    if target_root is None:
        raise SystemExit("No target provided. Use --target, HERMES_SKILLS_DIR, or CODEX_HOME.")

    actions: list[dict[str, Any]] = []
    blocked = 0
    copied = 0
    skipped = 0

    if not args.dry_run:
        target_root.mkdir(parents=True, exist_ok=True)

    for name in skills:
        source = source_root / name
        target = target_root / name
        if not source.exists():
            actions.append({"skill": name, "status": "blocked", "reason": "source_missing", "source": str(source)})
            blocked += 1
            continue
        if source.resolve() == target.resolve() or is_inside(target, source):
            actions.append({"skill": name, "status": "blocked", "reason": "unsafe_target_inside_source", "target": str(target)})
            blocked += 1
            continue
        if target.exists() and not args.force and not args.skip_existing:
            actions.append({"skill": name, "status": "blocked", "reason": "target_exists", "target": str(target)})
            blocked += 1
            continue
        if target.exists() and args.skip_existing and not args.force:
            actions.append({"skill": name, "status": "skipped", "reason": "target_exists", "target": str(target)})
            skipped += 1
            continue
        if args.dry_run:
            actions.append({"skill": name, "status": "would_copy", "source": str(source), "target": str(target)})
            continue
        if target.exists() and args.force:
            shutil.rmtree(target)
        shutil.copytree(source, target, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))
        actions.append({"skill": name, "status": "copied", "source": str(source), "target": str(target)})
        copied += 1

    payload = {
        "status": "ok" if blocked == 0 else "blocked",
        "source_root": str(source_root),
        "target": str(target_root),
        "dry_run": args.dry_run,
        "skill_count": len(skills),
        "copied_count": copied,
        "skipped_count": skipped,
        "blocked_count": blocked,
        "actions": actions,
    }
    return payload, 0 if blocked == 0 else 1


def render_markdown(payload: dict[str, Any]) -> str:
    lines = ["# Skill Kurulum Sonucu", ""]
    lines.append(f"- Durum: {payload['status']}")
    lines.append(f"- Hedef: {payload['target']}")
    lines.append(f"- Skill sayisi: {payload['skill_count']}")
    lines.append(f"- Kopyalanan: {payload['copied_count']} | Atlanan: {payload['skipped_count']} | Bloke: {payload['blocked_count']}")
    lines.extend(["", "## Islemler", ""])
    for item in payload["actions"]:
        lines.append(f"- {item['skill']}: {item['status']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", default=str(ROOT), help="Repository or package root containing skill-index.json.")
    parser.add_argument("--target", help="Target skill directory. Defaults to HERMES_SKILLS_DIR or CODEX_HOME/skills.")
    parser.add_argument("--skill", action="append", help="Skill name to install. Repeat for multiple skills. Defaults to all.")
    parser.add_argument("--force", action="store_true", help="Replace existing target skill folders.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip existing target skill folders instead of blocking.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned copy operations without writing files.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    payload, status = install(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
