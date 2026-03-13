"""Small CLI for scope inspection and local pipeline verification steps."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
import csv
from pathlib import Path
import json
import sys


TARGETS_FILE = Path("ingestion/location_targets.csv")
BRONZE_DIR = Path("data/bronze")
QUALITY_REPORT = Path("data/quality/silver_dq_report.json")


def parse_args() -> Namespace:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("show-scope", help="Print the five-city analytical scope from ingestion/location_targets.csv.")
    subparsers.add_parser("verify-bronze", help="Confirm Bronze files and metadata exist.")
    subparsers.add_parser("verify-quality-report", help="Confirm the Silver DQ report exists and passed.")
    return parser.parse_args()


def load_scope_rows(targets_file: Path) -> list[dict[str, str]]:
    with targets_file.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [
            {
                "location_id": str(row.get("location_id", "")).strip(),
                "city": str(row.get("city", "")).strip(),
                "country": str(row.get("country", "")).strip(),
            }
            for row in reader
            if str(row.get("city", "")).strip()
        ]


def show_scope() -> int:
    rows = load_scope_rows(TARGETS_FILE)
    if not rows:
        print(f"[FAIL] No scope rows found in {TARGETS_FILE}")
        return 1

    print("Configured five-city scope:")
    for row in rows:
        print(f"- {row['city']} ({row['country']}) [location_id={row['location_id']}]")
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


def verify_quality_report() -> int:
    if not QUALITY_REPORT.exists():
        print(f"[FAIL] Missing quality report: {QUALITY_REPORT}")
        return 1

    report = json.loads(QUALITY_REPORT.read_text(encoding="utf-8"))
    status = str(report.get("status", "")).lower()
    print(json.dumps(report, indent=2))
    if status != "pass":
        print("[FAIL] Silver data quality report is not in pass state.")
        return 1
    print("[PASS] Silver data quality report exists and passed.")
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "show-scope":
        return show_scope()
    if args.command == "verify-bronze":
        return verify_bronze()
    if args.command == "verify-quality-report":
        return verify_quality_report()
    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    sys.exit(main())
