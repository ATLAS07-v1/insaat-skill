#!/usr/bin/env python3
"""Create a safe Blender job plan without running Blender."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-type", default="construction_concept_scene")
    parser.add_argument("--input", action="append", default=[], help="Input file or brief path")
    parser.add_argument("--output-dir", default="blender-output")
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--height", type=int, default=1000)
    args = parser.parse_args()

    blender = shutil.which("blender")
    output_dir = Path(args.output_dir)
    scene_script = "create_construction_scene.py"
    spec = output_dir / "scene_spec.json"
    command = None
    if blender:
        command = (
            f'"{blender}" --background --python "{scene_script}" -- '
            f'--spec "{spec}" --output "{output_dir}"'
        )

    result = {
        "job_type": args.job_type,
        "inputs": args.input,
        "output_dir": str(output_dir),
        "render_resolution": [args.width, args.height],
        "available_blender": blender,
        "recommended_route": [
            "Write scene_spec.json with units, dimensions, materials, cameras, and outputs.",
            "Run Blender in background mode with create_construction_scene.py.",
            "Save .blend and PNG render in output directory.",
            "Verify render file exists and scene is not empty.",
        ],
        "command_to_review": command,
        "quality_gates": [
            "units_recorded",
            "dimensions_recorded_or_flagged_as_assumed",
            "camera_exists",
            "lighting_exists",
            "render_file_nonzero",
            "asset_licenses_checked",
        ],
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
