"""Small project CLI used by docs and Airflow helper tasks."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
import json
import sys

from ingestion.city_scope import CITY_SCOPE


BRONZE_DIR = Path("data/bronze")
QUALITY_REPORT = Path("data/quality/silver_dq_report.json")
SILVER_SUMMARY = Path("data/silver/latest_run_summary.json")


def parse_args() -> Namespace:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("show-scope", help="Print the fixed five-city analytical scope.")
    subparsers.add_parser("verify-bronze", help="Confirm Bronze files and metadata exist.")
    subparsers.add_parser("verify-silver", help="Print the latest Spark Silver run summary.")
    subparsers.add_parser("verify-quality-report", help="Confirm the Silver DQ report passed.")
    return parser.parse_args()


def show_scope() -> int:
    print("Fixed city scope:")
    for item in CITY_SCOPE:
        print(f"- {item.city}, {item.country}: {item.rationale}")
    return 0


def verify_bronze() -> int:
    bronze_files = sorted(BRONZE_DIR.rglob("*.csv.gz"))
    metadata_file = BRONZE_DIR / "location_metadata.csv"
    if not bronze_files:
        print(f"[FAIL] No Bronze archive files found in {BRONZE_DIR}")
        return 1
    if not metadata_file.exists():
        print(f"[FAIL] Missing Bronze metadata file: {metadata_file}")
        return 1
    print(f"[PASS] Bronze files present: {len(bronze_files)}")
    print(f"[INFO] Metadata file: {metadata_file}")
    return 0


def verify_silver() -> int:
    if not SILVER_SUMMARY.exists():
        print(f"[FAIL] Missing Spark run summary: {SILVER_SUMMARY}")
        return 1
    summary = json.loads(SILVER_SUMMARY.read_text(encoding='utf-8'))
    print(json.dumps(summary, indent=2))
    return 0


def verify_quality_report() -> int:
    if not QUALITY_REPORT.exists():
        print(f"[FAIL] Missing DQ report: {QUALITY_REPORT}")
        return 1
    report = json.loads(QUALITY_REPORT.read_text(encoding="utf-8"))
    print(json.dumps(report, indent=2))
    return 0 if report.get("status") == "pass" else 1


def main() -> int:
    args = parse_args()
    if args.command == "show-scope":
        return show_scope()
    if args.command == "verify-bronze":
        return verify_bronze()
    if args.command == "verify-silver":
        return verify_silver()
    if args.command == "verify-quality-report":
        return verify_quality_report()
    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    sys.exit(main())
