from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_manifest_generator_is_idempotent() -> None:
    generated_paths = [ROOT / "skill-index.json", *sorted(ROOT.glob("*/agents/openai.yaml"))]
    before = {path.relative_to(ROOT).as_posix(): path.read_text(encoding="utf-8") for path in generated_paths}

    result = subprocess.run(
        [sys.executable, "scripts/build_skill_manifests.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout

    after = {path.relative_to(ROOT).as_posix(): path.read_text(encoding="utf-8") for path in generated_paths}
    assert after == before
