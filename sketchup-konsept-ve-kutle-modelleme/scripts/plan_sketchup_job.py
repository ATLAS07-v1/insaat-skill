#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from check_sketchup_tools import find_sketchup_windows


ROUTES = {
    "site_massing": [
        "Collect site dimensions, setbacks, floor count, floor height, and orientation.",
        "Generate a Ruby API massing script with groups, tags, materials, and scenes.",
        "Run the script inside SketchUp desktop and save a new SKP output.",
        "Review face orientation, scale, scenes, and export needs.",
    ],
    "interior_concept": [
        "Collect room dimensions, openings, fixed furniture, material palette, and camera targets.",
        "Create a model brief or Ruby script for walls, floor, openings, and simple blocks.",
        "Use SketchUp scenes for client review; move final render work to Blender if needed.",
    ],
    "facade_concept": [
        "Collect elevation dimensions, bay rhythm, material palette, and reference images.",
        "Generate facade massing, window rhythm, material tags, and front/side scenes.",
        "Flag missing structural, fire, thermal, and code approvals.",
    ],
    "export_package": [
        "Identify source SKP and target format.",
        "Plan SketchUp export or glTF/Blender route.",
        "Verify units, materials, components, and geometry after export.",
    ],
}


def main():
    parser = argparse.ArgumentParser(description="Plan a SketchUp concept/massing job.")
    parser.add_argument("--job-type", default="site_massing", choices=sorted(ROUTES))
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("--output-dir", default="sketchup-output")
    args = parser.parse_args()

    sketchup_paths = find_sketchup_windows()
    ruby_script = str(Path(args.output_dir) / "sketchup_massing_scene.rb")
    command = None
    if sketchup_paths:
        command = f'"{sketchup_paths[-1]}" -RubyStartup "{Path(ruby_script).resolve()}"'

    result = {
        "job_type": args.job_type,
        "inputs": args.input,
        "output_dir": args.output_dir,
        "available_sketchup": sketchup_paths,
        "recommended_route": ROUTES[args.job_type],
        "command_to_review": command,
        "quality_gates": [
            "units_recorded",
            "dimensions_recorded_or_flagged_as_assumed",
            "groups_named",
            "tags_defined",
            "scenes_defined",
            "face_orientation_checked",
            "export_scale_checked",
            "asset_licenses_checked",
        ],
    }
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
