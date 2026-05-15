#!/usr/bin/env python3
"""Build release-ready package artifacts, checksums, metadata and notes."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from package_skills import DEFAULT_NAME, ROOT, build_package, file_sha256


def normalize_version(version: str) -> tuple[str, str]:
    clean = version.strip()
    if not clean:
        raise SystemExit("--version is required")
    tag = clean if clean.startswith("v") else f"v{clean}"
    bare = tag[1:]
    return tag, bare


def extract_changelog(version_tag: str) -> str:
    changelog = ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return f"# {version_tag}\n\nRelease notes are not available."
    lines = changelog.read_text(encoding="utf-8-sig").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if line.startswith("## "):
            starts.append((index, line[3:].strip()))
    aliases = {version_tag, version_tag.lstrip("v"), f"[{version_tag}]", f"[{version_tag.lstrip('v')}]"}
    for position, heading in starts:
        heading_key = heading.split(" - ", 1)[0].strip()
        if heading_key in aliases:
            next_position = next((idx for idx, _ in starts if idx > position), len(lines))
            body = "\n".join(lines[position:next_position]).strip()
            return f"# İnşaat Skill Seti {version_tag}\n\n{body}\n"
    return f"# İnşaat Skill Seti {version_tag}\n\nCHANGELOG.md içinde bu sürüm için not bulunamadı.\n"


def build_artifacts(args: argparse.Namespace) -> dict[str, Any]:
    version_tag, version = normalize_version(args.version)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    package_args = argparse.Namespace(
        source_root=str(ROOT),
        output_dir=str(output_dir),
        name=args.package_name,
        skill=None,
        include_examples=False,
        no_examples=args.no_examples,
        no_zip=False,
        force=True,
        format="json",
    )
    package_payload = build_package(package_args)
    archive = Path(package_payload["archive"]["path"])
    archive_sha = file_sha256(archive)

    checksums_path = output_dir / "SHA256SUMS.txt"
    checksums_path.write_text(f"{archive_sha}  {archive.name}\n", encoding="utf-8")

    release_notes_path = output_dir / "release-notes.md"
    release_notes_path.write_text(extract_changelog(version_tag), encoding="utf-8")

    metadata = {
        "name": args.package_name,
        "version": version,
        "tag": version_tag,
        "status": "ok",
        "git_sha": os.environ.get("GITHUB_SHA") or "",
        "git_ref": os.environ.get("GITHUB_REF") or "",
        "package_dir": package_payload["package_dir"],
        "archive": {
            "path": str(archive),
            "filename": archive.name,
            "sha256": archive_sha,
            "size_bytes": archive.stat().st_size,
        },
        "checksums": str(checksums_path),
        "release_notes": str(release_notes_path),
        "skill_count": package_payload["skill_count"],
        "skills": package_payload["skills"],
    }
    metadata_path = output_dir / "release-metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    metadata["metadata"] = str(metadata_path)
    return metadata


def render_markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Release Artifact Sonucu",
            "",
            f"- Tag: {payload['tag']}",
            f"- Skill sayisi: {payload['skill_count']}",
            f"- Arsiv: {payload['archive']['path']}",
            f"- SHA256: {payload['archive']['sha256']}",
            f"- Metadata: {payload['metadata']}",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Release version or tag, for example v0.1.0.")
    parser.add_argument("--output-dir", default=str(ROOT / "dist" / "release"), help="Directory for release artifacts.")
    parser.add_argument("--package-name", default=DEFAULT_NAME, help="Release package and archive name.")
    parser.add_argument("--no-examples", action="store_true", help="Skip examples in the release package.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    payload = build_artifacts(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
