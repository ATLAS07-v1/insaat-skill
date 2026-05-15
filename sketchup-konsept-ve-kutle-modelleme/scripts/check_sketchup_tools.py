#!/usr/bin/env python3
import json
import shutil
from pathlib import Path


def find_sketchup_windows():
    roots = [
        Path("C:/Program Files/SketchUp"),
        Path("C:/Program Files (x86)/SketchUp"),
    ]
    found = []
    for root in roots:
        if not root.exists():
            continue
        for exe in root.glob("SketchUp */SketchUp.exe"):
            found.append(str(exe))
    return found


def main():
    commands = {
        "ruby": shutil.which("ruby"),
        "bundle": shutil.which("bundle"),
        "node": shutil.which("node"),
        "python": shutil.which("python"),
    }
    sketchup_paths = find_sketchup_windows()
    result = {
        "commands": commands,
        "sketchup_executables": sketchup_paths,
        "has_sketchup": bool(sketchup_paths),
        "notes": [
            "SketchUp Ruby API is available only inside SketchUp desktop.",
            "Use -RubyStartup with an absolute ASCII-safe path when automating startup scripts.",
            "Use ruby-api-stubs, VSCode template, and TestUp for durable extension development.",
        ],
    }
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
