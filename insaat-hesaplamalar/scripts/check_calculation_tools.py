#!/usr/bin/env python3
import importlib.util
import json
import shutil


COMMANDS = ["python", "pip"]

PYTHON_MODULES = [
    "numpy",
    "pandas",
    "scipy",
    "sympy",
    "pint",
    "ifcopenshell",
    "ifc5d",
    "anastruct",
    "Pynite",
    "openseespy",
    "sectionproperties",
    "concreteproperties",
    "structuralcodes",
]


def module_exists(name):
    return importlib.util.find_spec(name) is not None


def main():
    result = {
        "commands": {name: shutil.which(name) for name in COMMANDS},
        "python_modules": {name: module_exists(name) for name in PYTHON_MODULES},
        "notes": [
            "Basic quantity scripts use only Python stdlib.",
            "Advanced structural calculations require specialist validation.",
            "Use Pint/SymPy for unit-aware and symbolic workflows when available.",
        ],
    }
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
