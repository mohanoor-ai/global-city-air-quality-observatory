"""Load the Spark Silver dataset into the partitioned BigQuery warehouse."""

from pathlib import Path
import argparse
import os
import subprocess
import sys


DEFAULT_PROJECT_ID = "aq-pipeline-260309-5800"
DEFAULT_BUCKET = "aq-lake-moha"
DEFAULT_DATASET = "air_quality_dw"
DEFAULT_FACT_TABLE = "fct_air_quality_measurements"
DEFAULT_CITY_DIM_TABLE = "dim_city"
DEFAULT_POLLUTANT_DIM_TABLE = "dim_pollutant"
DEFAULT_STAGING_TABLE = "silver_air_quality_measurements_staging"
DEFAULT_LOCATION = "EU"
SILVER_DIR = Path("data/silver/air_quality_measurements")


def run(cmd: list[str], env: dict[str, str] | None = None) -> str:
    """Run a shell command and return stdout, failing fast on errors."""
    print(f"[RUN] {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False, text=True, capture_output=True, env=env)
    if result.returncode != 0:
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print(result.stderr.strip())
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {cmd}")
    if result.stdout.strip():
        print(result.stdout.strip())
    return result.stdout


def silver_dataset_path() -> Path:
    files = sorted(SILVER_DIR.rglob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"No Silver parquet files found in {SILVER_DIR}")
    return SILVER_DIR


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
    parser.add_argument("--fact-table", default=DEFAULT_FACT_TABLE)
    parser.add_argument("--city-dim-table", default=DEFAULT_CITY_DIM_TABLE)
    parser.add_argument("--pollutant-dim-table", default=DEFAULT_POLLUTANT_DIM_TABLE)
    parser.add_argument("--staging-table", default=DEFAULT_STAGING_TABLE)
    parser.add_argument("--location", default=DEFAULT_LOCATION)
    args = parser.parse_args()

    # Reuse the same gcloud config directory set up in this project.
    env = os.environ.copy()
    env.setdefault("CLOUDSDK_CONFIG", "/tmp/gcloud")

    try:
        silver_dir = silver_dataset_path()
        gcs_prefix = f"gs://{args.bucket}/silver/air_quality_measurements"
        gcs_uri = f"{gcs_prefix}/batch_date=*/*.parquet"
        target_fq = f"{args.project_id}.{args.dataset}.{args.fact_table}"
        staging_fq = f"{args.project_id}.{args.dataset}.{args.staging_table}"
        staging_ref = f"{args.dataset}.{args.staging_table}"
        city_dim_fq = f"{args.project_id}.{args.dataset}.{args.city_dim_table}"
        pollutant_dim_fq = f"{args.project_id}.{args.dataset}.{args.pollutant_dim_table}"

        print(f"[INFO] Using Silver dataset: {silver_dir}")
        print(f"[INFO] Upload target: {gcs_prefix}")

        run(["gcloud", "storage", "cp", "--recursive", str(silver_dir), gcs_prefix], env=env)

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

        create_sql = (
            f"CREATE OR REPLACE TABLE `{target_fq}` "
            "PARTITION BY measurement_date "
            "CLUSTER BY city, pollutant AS "
            "SELECT "
            "  CAST(city AS STRING) AS city, "
            "  CAST(country AS STRING) AS country, "
            "  CAST(location_id AS INT64) AS location_id, "
            "  CAST(location_name AS STRING) AS location_name, "
            "  CAST(sensor_id AS INT64) AS sensor_id, "
            "  LOWER(CAST(pollutant AS STRING)) AS pollutant, "
            "  CAST(measurement_value AS FLOAT64) AS measurement_value, "
            "  CAST(measurement_unit AS STRING) AS measurement_unit, "
            "  SAFE_CAST(measurement_datetime AS TIMESTAMP) AS measurement_datetime, "
            "  SAFE_CAST(measurement_date AS DATE) AS measurement_date, "
            "  CAST(latitude AS FLOAT64) AS latitude, "
            "  CAST(longitude AS FLOAT64) AS longitude, "
            "  SAFE_CAST(batch_date AS DATE) AS batch_date, "
            "  CAST(source_file AS STRING) AS source_file "
            f"FROM `{staging_fq}` "
            "WHERE SAFE_CAST(measurement_datetime AS TIMESTAMP) IS NOT NULL "
            "  AND SAFE_CAST(measurement_date AS DATE) IS NOT NULL;"
        )
        run(
            [
                "bq",
                f"--project_id={args.project_id}",
                f"--location={args.location}",
                "query",
                "--nouse_legacy_sql",
                create_sql,
            ],
            env=env,
        )

        city_dim_sql = (
            f"CREATE OR REPLACE TABLE `{city_dim_fq}` AS "
            "SELECT DISTINCT "
            "  city, "
            "  country, "
            "  COUNT(DISTINCT location_id) AS station_count, "
            "  ROUND(AVG(latitude), 6) AS avg_latitude, "
            "  ROUND(AVG(longitude), 6) AS avg_longitude "
            f"FROM `{target_fq}` "
            "GROUP BY city, country"
        )
        run(
            [
                "bq",
                f"--project_id={args.project_id}",
                f"--location={args.location}",
                "query",
                "--nouse_legacy_sql",
                city_dim_sql,
            ],
            env=env,
        )

        pollutant_dim_sql = (
            f"CREATE OR REPLACE TABLE `{pollutant_dim_fq}` AS "
            "SELECT DISTINCT "
            "  pollutant, "
            "  ANY_VALUE(measurement_unit) AS measurement_unit "
            f"FROM `{target_fq}` "
            "GROUP BY pollutant"
        )
        run(
            [
                "bq",
                f"--project_id={args.project_id}",
                f"--location={args.location}",
                "query",
                "--nouse_legacy_sql",
                pollutant_dim_sql,
            ],
            env=env,
        )

        count = row_count(
            args.project_id, args.dataset, args.fact_table, args.location, env
        )
        print(f"[PASS] Warehouse load complete. Fact row count: {count:,}")
        return 0

    except Exception as exc:
        print(f"[FAIL] {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
