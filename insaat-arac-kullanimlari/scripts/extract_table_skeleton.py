#!/usr/bin/env python3
"""Optional table extraction skeleton for CSV/XLSX files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="CSV/XLSX file")
    args = parser.parse_args()

    path = Path(args.path)
    try:
        import pandas as pd  # type: ignore
    except Exception:
        print("pandas is not installed. Install with: pip install pandas openpyxl")
        return 2

    if path.suffix.lower() in {".xlsx", ".xlsm", ".xls"}:
        sheets = pd.read_excel(path, sheet_name=None)
        result = {
            sheet_name: {
                "rows": int(frame.shape[0]),
                "columns": list(map(str, frame.columns)),
                "preview": frame.head(10).fillna("").to_dict(orient="records"),
            }
            for sheet_name, frame in sheets.items()
        }
    else:
        frame = pd.read_csv(path)
        result = {
            "rows": int(frame.shape[0]),
            "columns": list(map(str, frame.columns)),
            "preview": frame.head(10).fillna("").to_dict(orient="records"),
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
