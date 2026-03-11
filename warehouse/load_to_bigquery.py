"""
Load Silver data into BigQuery warehouse tables.

This script:
- picks the latest Silver parquet file
- uploads the file to GCS under silver/
- loads it into a BigQuery staging table
- refreshes the target warehouse table from staging
- prints the final row count
"""

from pathlib import Path
import argparse
import os
import subprocess
import sys


DEFAULT_PROJECT_ID = "aq-pipeline-260309-5800"
DEFAULT_BUCKET = "aq-lake-moha"
DEFAULT_DATASET = "air_quality_dw"
DEFAULT_TARGET_TABLE = "air_quality_measurements"
DEFAULT_STAGING_TABLE = "air_quality_measurements_staging"
DEFAULT_LOCATION = "EU"
SILVER_DIR = Path("data/silver")


def run(cmd: list[str], env: dict[str, str] | None = None) -> str:
    """Run a shell command and return stdout, failing fast on errors."""
    print(f"[RUN] {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        check=True,
        text=True,
        capture_output=True,
        env=env,
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    return result.stdout


def latest_silver_file() -> Path:
    files = sorted(SILVER_DIR.glob("*.parquet"), key=lambda p: p.stat().st_mtime)
    if not files:
        raise FileNotFoundError(f"No Silver parquet files found in {SILVER_DIR}")
    return files[-1]


def row_count(
    project_id: str,
    dataset: str,
    table: str,
    location: str,
    env: dict[str, str] | None = None,
) -> int:
    sql = f"SELECT COUNT(*) AS row_count FROM `{project_id}.{dataset}.{table}`"
    out = run(
        [
            "bq",
            f"--project_id={project_id}",
            f"--location={location}",
            "query",
            "--nouse_legacy_sql",
            "--format=csv",
            sql,
        ],
        env=env,
    )
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    if len(lines) < 2:
        raise RuntimeError("Unexpected bq output while reading row count.")
    return int(lines[-1])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", default=DEFAULT_PROJECT_ID)
    parser.add_argument("--bucket", default=DEFAULT_BUCKET)
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--target-table", default=DEFAULT_TARGET_TABLE)
    parser.add_argument("--staging-table", default=DEFAULT_STAGING_TABLE)
    parser.add_argument("--location", default=DEFAULT_LOCATION)
    args = parser.parse_args()

    # Reuse the same gcloud config directory set up in this project.
    env = os.environ.copy()
    env.setdefault("CLOUDSDK_CONFIG", "/tmp/gcloud")

    try:
        silver_file = latest_silver_file()
        gcs_uri = f"gs://{args.bucket}/silver/{silver_file.name}"
        target_fq = f"{args.project_id}.{args.dataset}.{args.target_table}"
        staging_fq = f"{args.project_id}.{args.dataset}.{args.staging_table}"
        staging_ref = f"{args.dataset}.{args.staging_table}"

        print(f"[INFO] Using Silver file: {silver_file}")
        print(f"[INFO] Upload target: {gcs_uri}")

        run(["gcloud", "storage", "cp", str(silver_file), gcs_uri], env=env)

        run(
            [
                "bq",
                f"--project_id={args.project_id}",
                f"--location={args.location}",
                "load",
                "--replace",
                "--source_format=PARQUET",
                "--autodetect",
                staging_ref,
                gcs_uri,
            ],
            env=env,
        )

        # Rebuild the curated table from staging so the downstream schema stays consistent.
        sql = (
            f"CREATE OR REPLACE TABLE `{target_fq}` AS "
            "SELECT "
            "  TIMESTAMP(measurement_datetime) AS measurement_datetime, "
            "  DATE(measurement_datetime) AS measurement_date, "
            "  CAST(location_id AS INT64) AS location_id, "
            "  CAST(location_name AS STRING) AS location_name, "
            "  CAST(city AS STRING) AS city, "
            "  CAST(country AS STRING) AS country, "
            "  CAST(latitude AS FLOAT64) AS latitude, "
            "  CAST(longitude AS FLOAT64) AS longitude, "
            "  LOWER(CAST(pollutant AS STRING)) AS pollutant, "
            "  CAST(value AS FLOAT64) AS value, "
            "  CAST(unit AS STRING) AS unit "
            f"FROM `{staging_fq}` "
            "WHERE measurement_datetime IS NOT NULL;"
        )
        run(
            [
                "bq",
                f"--project_id={args.project_id}",
                f"--location={args.location}",
                "query",
                "--nouse_legacy_sql",
                sql,
            ],
            env=env,
        )

        count = row_count(
            args.project_id, args.dataset, args.target_table, args.location, env
        )
        print(f"[PASS] Warehouse load complete. Target row count: {count:,}")
        return 0

    except Exception as exc:
        print(f"[FAIL] {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
