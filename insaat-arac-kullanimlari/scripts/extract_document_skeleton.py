#!/usr/bin/env python3
"""Optional document extraction skeleton for PDF/Office files.

The script tries MarkItDown first, then leaves clear fallback messages for
Docling, PyMuPDF, and pdfplumber. Install dependencies only when needed.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def try_markitdown(path: Path) -> str | None:
    try:
        from markitdown import MarkItDown  # type: ignore
    except Exception:
        return None
    converter = MarkItDown()
    result = converter.convert(str(path))
    return result.text_content


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="PDF/Office/image file")
    args = parser.parse_args()

    path = Path(args.path)
    markdown = try_markitdown(path)
    if markdown is not None:
        print(markdown)
        return 0

    print("MarkItDown is not installed or failed for this file.")
    print("Suggested fallbacks:")
    print("- pip install docling  # layout/OCR/table-heavy documents")
    print("- pip install pymupdf  # PDF render and low-level page extraction")
    print("- pip install pdfplumber  # precise machine-generated PDF tables")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
