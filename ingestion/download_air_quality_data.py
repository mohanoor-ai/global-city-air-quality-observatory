"""Download OpenAQ archive files into the Bronze layer.

Modes:
- backfill: last 2 full years + current year-to-date
- daily: newest available file per configured location
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
import argparse
import csv

import boto3
from botocore import UNSIGNED
from botocore.config import Config

from ingestion.city_scope import DEFAULT_TARGETS_FILE, validate_scope_rows


BUCKET_NAME = "openaq-data-archive"
AWS_REGION = "us-east-1"
BRONZE_DIR = Path("data/bronze")
METADATA_FILE = BRONZE_DIR / "location_metadata.csv"

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    config=Config(signature_version=UNSIGNED),
)


@dataclass
class LocationTarget:
    location_id: str
    city: str
    country: str


def load_targets(path: Path) -> list[LocationTarget]:
    """Read location targets used by both backfill and daily modes."""
    if not path.exists():
        raise FileNotFoundError(
            f"Missing targets file: {path}. Create it with location_id,city,country columns."
        )

    targets: list[LocationTarget] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"location_id", "city", "country"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"{path} must include columns: {sorted(required)}")

        for row in reader:
            location_id = str(row.get("location_id", "")).strip()
            if not location_id:
                continue
            targets.append(
                LocationTarget(
                    location_id=location_id,
                    city=str(row.get("city", "")).strip(),
                    country=str(row.get("country", "")).strip(),
                )
            )

    if not targets:
        raise ValueError(f"{path} has no usable location rows.")
    validate_scope_rows([(target.city, target.country) for target in targets])
    return targets


def write_metadata_file(targets: list[LocationTarget]) -> None:
    """Store location metadata in Bronze for Silver enrichment."""
    METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with METADATA_FILE.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["location_id", "city", "country"])
        writer.writeheader()
        for target in targets:
            writer.writerow(
                {
                    "location_id": target.location_id,
                    "city": target.city,
                    "country": target.country,
                }
            )


def list_keys(prefix: str) -> list[str]:
    paginator = s3.get_paginator("list_objects_v2")
    keys: list[str] = []
    for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.endswith(".csv.gz"):
                keys.append(key)
    return sorted(keys)


def local_path_for_key(key: str) -> Path:
    return BRONZE_DIR / key


def download_key(key: str, overwrite: bool) -> bool:
    local_file = local_path_for_key(key)
    if local_file.exists() and not overwrite:
        return False

    local_file.parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(BUCKET_NAME, key, str(local_file))
    return True


def backfill_months(now: datetime) -> list[tuple[int, int]]:
    start_year = now.year - 2
    periods: list[tuple[int, int]] = []
    for year in range(start_year, now.year + 1):
        end_month = now.month if year == now.year else 12
        for month in range(1, end_month + 1):
            periods.append((year, month))
    return periods


def run_backfill(targets: list[LocationTarget], overwrite: bool) -> tuple[int, int]:
    """Download all files for last 2 full years + current year-to-date."""
    now = datetime.now(UTC)
    periods = backfill_months(now)
    scanned = 0
    downloaded = 0

    for target in targets:
        for year, month in periods:
            prefix = (
                f"records/csv.gz/locationid={target.location_id}/"
                f"year={year}/month={month:02d}/"
            )
            keys = list_keys(prefix)
            scanned += len(keys)
            for key in keys:
                did_download = download_key(key, overwrite=overwrite)
                if did_download:
                    downloaded += 1

    return scanned, downloaded


def run_daily(targets: list[LocationTarget], overwrite: bool) -> tuple[int, int]:
    """Download one newest file per location target."""
    now = datetime.now(UTC)
    scanned = 0
    downloaded = 0
    year_candidates = [now.year, now.year - 1]

    for target in targets:
        all_keys: list[str] = []
        # Check current year first, then previous year to handle year boundary days.
        for year in year_candidates:
            prefix = f"records/csv.gz/locationid={target.location_id}/year={year}/"
            keys = list_keys(prefix)
            scanned += len(keys)
            all_keys.extend(keys)

        if not all_keys:
            print(f"[WARN] No files found for location_id={target.location_id}")
            continue

        latest_key = sorted(all_keys)[-1]
        if download_key(latest_key, overwrite=overwrite):
            downloaded += 1
            print(f"[INFO] Downloaded latest file for {target.location_id}: {latest_key}")
        else:
            print(f"[INFO] Latest file already exists for {target.location_id}: {latest_key}")

    return scanned, downloaded


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["backfill", "daily"],
        default="backfill",
        help="backfill=last 2 full years + current YTD, daily=newest file per location",
    )
    parser.add_argument(
        "--targets-file",
        default=str(DEFAULT_TARGETS_FILE),
        help="CSV file with columns: location_id,city,country",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Redownload files even if already present in Bronze.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    targets = load_targets(Path(args.targets_file))
    write_metadata_file(targets)

    if args.mode == "backfill":
        scanned, downloaded = run_backfill(targets, overwrite=args.overwrite)
    else:
        scanned, downloaded = run_daily(targets, overwrite=args.overwrite)

    print(f"[PASS] Mode: {args.mode}")
    print(f"[INFO] Targets: {len(targets)} locations")
    print(f"[INFO] Files scanned: {scanned}")
    print(f"[INFO] Files downloaded: {downloaded}")
    print(f"[INFO] Metadata file: {METADATA_FILE}")


if __name__ == "__main__":
    main()
