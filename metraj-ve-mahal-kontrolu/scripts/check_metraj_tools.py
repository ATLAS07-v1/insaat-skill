#!/usr/bin/env python3
import importlib.util
import json
import shutil


COMMANDS = [
    "python",
    "pip",
    "ifccsv",
    "IfcConvert",
    "ifcconvert",
]

PYTHON_MODULES = [
    "pandas",
    "openpyxl",
    "ifcopenshell",
    "ifc5d",
    "ifccsv",
    "pdfplumber",
    "camelot",
    "fitz",
    "rapidfuzz",
]


def module_exists(name):
    return importlib.util.find_spec(name) is not None


def main():
    result = {
        "commands": {name: shutil.which(name) for name in COMMANDS},
        "python_modules": {name: module_exists(name) for name in PYTHON_MODULES},
        "notes": [
            "CSV/JSON schedule comparison uses Python stdlib.",
            "IFC space extraction requires ifcopenshell.",
            "PDF table extraction is reliable only for text-based PDFs; scanned PDFs need OCR.",
        ],
    }
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
