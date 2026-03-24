"""Run data quality checks against the Silver parquet dataset."""

from __future__ import annotations

from pathlib import Path
from argparse import ArgumentParser, Namespace
import csv
import json
import sys

import pandas as pd


SILVER_DIR = Path("data/silver/air_quality_measurements")
QUALITY_DIR = Path("data/quality")
REPORT_PATH = QUALITY_DIR / "silver_dq_report.json"
TARGETS_FILE = Path("ingestion/location_targets.csv")
EXPECTED_POLLUTANTS = {"pm25", "pm10", "no2", "co", "o3"}
REQUIRED_COLUMNS = {
    "city",
    "country",
    "location_id",
    "location_name",
    "pollutant",
    "measurement_value",
    "measurement_unit",
    "measurement_datetime",
    "measurement_date",
    "latitude",
    "longitude",
    "batch_date",
    "source_file",
}


def load_expected_cities(targets_file: Path = TARGETS_FILE) -> set[str]:
    with targets_file.open("r", encoding="utf-8", newline="") as handle:
        return {
            str(row.get("city", "")).strip()
            for row in csv.DictReader(handle)
            if str(row.get("city", "")).strip()
        }


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--silver-dir", default=str(SILVER_DIR))
    parser.add_argument("--report-path", default=str(REPORT_PATH))
    parser.add_argument(
        "--verify-report",
        action="store_true",
        help="Check an existing quality report instead of recomputing it.",
    )
    return parser.parse_args()


def load_dataset(path: Path) -> pd.DataFrame:
    parquet_files = sorted(path.rglob("*.parquet"))
    if not parquet_files:
        raise FileNotFoundError(f"No Silver parquet files found in {path}")
    return pd.read_parquet(path)


def verify_report(report_path: Path) -> int:
    if not report_path.exists():
        print(f"[FAIL] Missing quality report: {report_path}")
        return 1

    report = json.loads(report_path.read_text(encoding="utf-8"))
    print(json.dumps(report, indent=2))
    if str(report.get("status", "")).lower() != "pass":
        print("[FAIL] Silver data quality report is not in pass state.")
        return 1

    print("[PASS] Silver data quality report exists and passed.")
    return 0


def main() -> int:
    args = parse_args()
    silver_dir = Path(args.silver_dir)
    report_path = Path(args.report_path)
    expected_cities = load_expected_cities()
    if args.verify_report:
        return verify_report(report_path)
    errors: list[str] = []

    try:
        df = load_dataset(silver_dir)
    except FileNotFoundError as exc:
        print(f"[FAIL] {exc}")
        return 1

    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")

    if df.empty:
        errors.append("Silver dataset is empty.")

    if "city" in df.columns:
        actual_cities = set(df["city"].dropna().astype(str).unique().tolist())
        if actual_cities != expected_cities:
            errors.append(f"Silver dataset cities do not match the fixed scope: {sorted(actual_cities)}")

    if "pollutant" in df.columns:
        actual_pollutants = set(df["pollutant"].dropna().astype(str).str.lower().unique().tolist())
        unexpected = sorted(actual_pollutants - EXPECTED_POLLUTANTS)
        if unexpected:
            errors.append(f"Unexpected pollutants present: {unexpected}")

    duplicate_count = 0
    duplicate_keys = [
        "city",
        "location_id",
        "measurement_datetime",
        "pollutant",
        "measurement_value",
    ]
    if all(column in df.columns for column in duplicate_keys):
        duplicate_count = int(df.duplicated(subset=duplicate_keys).sum())
        if duplicate_count:
            errors.append(f"Duplicate measurement rows detected: {duplicate_count}")

    null_checks = {}
    for column in ["city", "location_id", "pollutant", "measurement_value", "measurement_datetime"]:
        if column in df.columns:
            null_checks[column] = int(df[column].isna().sum())
            if null_checks[column] > 0:
                errors.append(f"Column '{column}' has {null_checks[column]} null values.")

    report = {
        "status": "fail" if errors else "pass",
        "silver_dir": str(silver_dir),
        "row_count": int(len(df)),
        "cities": sorted(df["city"].dropna().astype(str).unique().tolist()) if "city" in df.columns else [],
        "pollutants": sorted(df["pollutant"].dropna().astype(str).str.lower().unique().tolist()) if "pollutant" in df.columns else [],
        "duplicate_count": duplicate_count,
        "null_checks": null_checks,
        "errors": errors,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"[INFO] DQ report saved to {report_path}")

    if errors:
        print("[FAIL] Silver data quality checks failed.")
        for error in errors:
            print(f"- {error}")
        return 1

    print("[PASS] Silver data quality checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
