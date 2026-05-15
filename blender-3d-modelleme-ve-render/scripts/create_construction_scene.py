#!/usr/bin/env python3
"""Blender Python script to create a simple construction/interior scene.

Run inside Blender:
  blender --background --python create_construction_scene.py -- --spec scene.json --output output

The JSON spec is optional. Missing dimensions are treated as assumptions.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1 :]
    else:
        argv = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", default=None)
    parser.add_argument("--output", default="blender-output")
    return parser.parse_args(argv)


def load_spec(path: str | None) -> dict:
    if not path:
        return {}
    spec_path = Path(path)
    if not spec_path.exists():
        return {"quality_flags": ["spec_file_missing"]}
    return json.loads(spec_path.read_text(encoding="utf-8"))


def make_mat(bpy, name: str, color: tuple[float, float, float, float]):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = 0.55
    return mat


def cube(bpy, name: str, location, scale, material):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        obj.data.materials.append(material)
    return obj


def main() -> int:
    try:
        import bpy  # type: ignore
    except Exception as exc:
        print(f"This script must run inside Blender Python: {exc}")
        return 2

    args = parse_args()
    spec = load_spec(args.spec)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    width = float(spec.get("width_m", 5.0))
    depth = float(spec.get("depth_m", 4.0))
    height = float(spec.get("height_m", 3.0))
    wall = float(spec.get("wall_thickness_m", 0.15))
    quality_flags = list(spec.get("quality_flags", []))
    if "width_m" not in spec or "depth_m" not in spec or "height_m" not in spec:
        quality_flags.append("assumed_dimensions")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0

    mat_floor = make_mat(bpy, "Mat_Floor_Concrete", (0.55, 0.55, 0.52, 1.0))
    mat_wall = make_mat(bpy, "Mat_Wall_Paint", (0.86, 0.84, 0.78, 1.0))
    mat_glass = make_mat(bpy, "Mat_Glass_Clear", (0.55, 0.75, 0.95, 0.35))
    mat_accent = make_mat(bpy, "Mat_Accent_Wood", (0.45, 0.26, 0.12, 1.0))

    cube(bpy, "Floor_Main", (0, 0, -0.05), (width, depth, 0.10), mat_floor)
    cube(bpy, "Wall_North", (0, depth / 2, height / 2), (width, wall, height), mat_wall)
    cube(bpy, "Wall_South", (0, -depth / 2, height / 2), (width, wall, height), mat_wall)
    cube(bpy, "Wall_East", (width / 2, 0, height / 2), (wall, depth, height), mat_wall)
    cube(bpy, "Wall_West", (-width / 2, 0, height / 2), (wall, depth, height), mat_wall)
    cube(bpy, "Window_Concept", (0, depth / 2 + 0.01, 1.55), (1.8, 0.03, 1.1), mat_glass)
    cube(bpy, "Door_Concept", (-width / 2 - 0.01, -0.9, 1.05), (0.03, 0.9, 2.1), mat_accent)
    cube(bpy, "Feature_Counter", (0.7, -0.7, 0.45), (1.6, 0.55, 0.9), mat_accent)

    bpy.ops.object.light_add(type="AREA", location=(0, -2.5, 4.5))
    area = bpy.context.object
    area.name = "Area_Key"
    area.data.energy = 500
    area.data.size = 4

    bpy.ops.object.light_add(type="SUN", location=(2, -3, 5))
    sun = bpy.context.object
    sun.name = "Sun_Main"
    sun.data.energy = 1.2

    bpy.ops.object.camera_add(location=(width * 0.75, -depth * 1.25, height * 0.85), rotation=(math.radians(62), 0, math.radians(34)))
    camera = bpy.context.object
    camera.name = "Camera_Main"
    bpy.context.scene.camera = camera
    camera.data.lens = 24

    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.samples = int(spec.get("samples", 64))
    bpy.context.scene.render.resolution_x = int(spec.get("resolution_x", 1600))
    bpy.context.scene.render.resolution_y = int(spec.get("resolution_y", 1000))
    bpy.context.scene.render.filepath = str((output_dir / "render.png").resolve())

    blend_path = output_dir / "scene.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path.resolve()))

    if spec.get("render", True):
        bpy.ops.render.render(write_still=True)

    report = {
        "scene_file": str(blend_path.resolve()),
        "render_file": str((output_dir / "render.png").resolve()),
        "unit": "meters",
        "dimensions_m": {"width": width, "depth": depth, "height": height, "wall_thickness": wall},
        "objects": [obj.name for obj in bpy.context.scene.objects],
        "materials": [mat.name for mat in bpy.data.materials],
        "camera": "Camera_Main",
        "quality_flags": quality_flags,
    }
    (output_dir / "render_report.json").write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
