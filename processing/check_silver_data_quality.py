"""
Validate the Silver dataset before warehouse loading.

This script:
- selects a Silver parquet file (latest by default)
- verifies required schema columns
- checks allowed pollutants and missing values
- validates datetime and numeric value fields
"""

from pathlib import Path
import json
import sys

import pandas as pd


SILVER_DIR = Path("data/silver")
QUALITY_DIR = Path("data/quality")
EXPECTED_POLLUTANTS = {"pm25", "pm10", "no2", "co", "o3"}
REQUIRED_COLUMNS = {
    "measurement_datetime",
    "location_name",
    "latitude",
    "longitude",
    "pollutant",
    "value",
    "unit",
}
NULL_CHECK_COLUMNS = ["measurement_datetime", "pollutant", "value"]


def resolve_silver_path() -> Path | None:
    if len(sys.argv) > 1:
        return Path(sys.argv[1])

    candidates = sorted(SILVER_DIR.glob("*.parquet"), key=lambda p: p.stat().st_mtime)
    if not candidates:
        return None
    return candidates[-1]


def build_report_path(silver_path: Path) -> Path:
    stem = silver_path.stem
    return QUALITY_DIR / f"{stem}_dq_report.json"


def main() -> int:
    errors: list[str] = []
    silver_path = resolve_silver_path()

    if silver_path is None:
        print(f"[FAIL] No Silver parquet files found in: {SILVER_DIR}")
        print("Create the Silver dataset first, then run this check.")
        return 1

    if not silver_path.exists():
        print(f"[FAIL] Missing file: {silver_path}")
        print("Pass a valid Silver parquet file path or create a new Silver dataset.")
        return 1

    print(f"[INFO] Checking file: {silver_path}")
    df = pd.read_parquet(silver_path)
    print(f"[INFO] Loaded rows: {len(df):,}")

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        errors.append(f"Missing required columns: {sorted(missing_columns)}")

    if df.empty:
        errors.append("Silver dataset is empty.")

    pollutant_distribution: dict[str, int] = {}
    if "pollutant" in df.columns:
        normalized_pollutants = df["pollutant"].astype(str).str.lower().dropna()
        pollutants = set(normalized_pollutants.unique())
        unexpected = sorted(pollutants - EXPECTED_POLLUTANTS)
        if unexpected:
            errors.append(f"Unexpected pollutants found: {unexpected}")
        pollutant_distribution = (
            normalized_pollutants.value_counts().sort_index().astype(int).to_dict()
        )
        print(f"[INFO] Pollutants present: {sorted(pollutants)}")
        print(f"[INFO] Pollutant distribution: {pollutant_distribution}")

    null_counts: dict[str, int] = {}
    for column in NULL_CHECK_COLUMNS:
        if column in df.columns:
            null_count = int(df[column].isna().sum())
            null_counts[column] = null_count
            if null_count > 0:
                errors.append(f"Column '{column}' has {null_count} null values.")

    min_datetime = None
    max_datetime = None
    invalid_dt_count = 0
    if "measurement_datetime" in df.columns:
        dt = pd.to_datetime(df["measurement_datetime"], errors="coerce", utc=True)
        invalid_dt_count = int(dt.isna().sum())
        if invalid_dt_count > 0:
            errors.append(
                f"Column 'measurement_datetime' has {invalid_dt_count} invalid datetime values."
            )
        if not dt.dropna().empty:
            min_datetime = dt.min().isoformat()
            max_datetime = dt.max().isoformat()
            print(f"[INFO] Date range: {dt.min()} -> {dt.max()}")

    non_numeric = 0
    if "value" in df.columns:
        non_numeric = int(pd.to_numeric(df["value"], errors="coerce").isna().sum())
        if non_numeric > 0:
            errors.append(f"Column 'value' has {non_numeric} non-numeric values.")

    report = {
        "status": "fail" if errors else "pass",
        "silver_file": str(silver_path),
        "row_count": int(len(df)),
        "required_columns": sorted(REQUIRED_COLUMNS),
        "missing_columns": sorted(missing_columns),
        "pollutants_present": sorted(pollutant_distribution.keys()),
        "pollutant_distribution": pollutant_distribution,
        "null_counts": null_counts,
        "invalid_datetime_count": invalid_dt_count,
        "non_numeric_value_count": non_numeric,
        "date_range": {
            "min": min_datetime,
            "max": max_datetime,
        },
        "errors": errors,
    }

    report_path = build_report_path(silver_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"[INFO] DQ report saved: {report_path}")

    if errors:
        print("\n[FAIL] Data quality checks failed:")
        for issue in errors:
            print(f"- {issue}")
        return 1

    print("\n[PASS] All data quality checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
