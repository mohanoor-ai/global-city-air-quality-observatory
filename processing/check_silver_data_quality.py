"""
Validate the Silver dataset before warehouse loading.

This script:
- selects a Silver parquet file (latest by default)
- verifies required schema columns
- checks allowed pollutants and missing values
- validates datetime and numeric value fields
"""

from pathlib import Path
import sys

import pandas as pd


SILVER_DIR = Path("data/silver")
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

    if "pollutant" in df.columns:
        pollutants = set(df["pollutant"].astype(str).str.lower().dropna().unique())
        unexpected = sorted(pollutants - EXPECTED_POLLUTANTS)
        if unexpected:
            errors.append(f"Unexpected pollutants found: {unexpected}")
        print(f"[INFO] Pollutants present: {sorted(pollutants)}")

    for column in NULL_CHECK_COLUMNS:
        if column in df.columns:
            null_count = int(df[column].isna().sum())
            if null_count > 0:
                errors.append(f"Column '{column}' has {null_count} null values.")

    if "measurement_datetime" in df.columns:
        dt = pd.to_datetime(df["measurement_datetime"], errors="coerce", utc=True)
        invalid_dt_count = int(dt.isna().sum())
        if invalid_dt_count > 0:
            errors.append(
                f"Column 'measurement_datetime' has {invalid_dt_count} invalid datetime values."
            )
        if not dt.dropna().empty:
            print(f"[INFO] Date range: {dt.min()} -> {dt.max()}")

    if "value" in df.columns:
        non_numeric = int(pd.to_numeric(df["value"], errors="coerce").isna().sum())
        if non_numeric > 0:
            errors.append(f"Column 'value' has {non_numeric} non-numeric values.")

    if errors:
        print("\n[FAIL] Data quality checks failed:")
        for issue in errors:
            print(f"- {issue}")
        return 1

    print("\n[PASS] All data quality checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
