#!/usr/bin/env python3
import importlib.util
import json
import shutil


COMMANDS = [
    "dwg2dxf",
    "dwgread",
    "dxf2dwg",
    "ezdxf",
    "IfcConvert",
    "ifcconvert",
    "FreeCADCmd",
    "freecadcmd",
    "blender",
    "assimp",
    "magick",
    "identify",
    "qpdf",
    "mutool",
    "pdfinfo",
    "pdftoppm",
    "pdfimages",
    "inkscape",
    "ogr2ogr",
    "gdalinfo",
    "gltf_validator",
    "gltf-validator",
    "node",
    "python",
]

PYTHON_MODULES = [
    "ezdxf",
    "ifcopenshell",
    "fitz",
    "PIL",
    "pypdf",
]


def module_exists(name):
    return importlib.util.find_spec(name) is not None


def main():
    commands = {name: shutil.which(name) for name in COMMANDS}
    modules = {name: module_exists(name) for name in PYTHON_MODULES}
    result = {
        "commands": commands,
        "python_modules": modules,
        "notes": [
            "No source files are modified by this checker.",
            "DWG/RVT/SKP and some FBX workflows may require proprietary source application exports.",
            "Run post-conversion QA; output file existence alone is not sufficient.",
        ],
    }
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
