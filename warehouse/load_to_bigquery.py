"""Load the Spark Silver dataset into the partitioned BigQuery warehouse."""

from pathlib import Path
import argparse
import os
import subprocess
import sys


DEFAULT_PROJECT_ID = "your-gcp-project-id"
DEFAULT_BUCKET = "your-global-city-air-quality-observatory-bucket"
DEFAULT_DATASET = "air_quality_dw"
DEFAULT_FACT_TABLE = "fct_air_quality_measurements"
DEFAULT_CITY_DIM_TABLE = "dim_city"
DEFAULT_POLLUTANT_DIM_TABLE = "dim_pollutant"
DEFAULT_STAGING_TABLE = "silver_air_quality_measurements_staging"
DEFAULT_LOCATION = "EU"
SILVER_DIR = Path("data/silver/air_quality_measurements")
TERRAFORM_TFVARS = Path("terraform/terraform.tfvars")


def load_tfvars(path: Path) -> dict[str, str]:
    """Load simple string assignments from terraform.tfvars without extra dependencies."""
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value:
            values[key] = value
    return values


def build_defaults() -> dict[str, str]:
    tfvars = load_tfvars(TERRAFORM_TFVARS)
    return {
        "project_id": os.getenv("PROJECT_ID", tfvars.get("project_id", DEFAULT_PROJECT_ID)),
        "bucket": os.getenv("GCS_BUCKET", tfvars.get("gcs_bucket_name", DEFAULT_BUCKET)),
        "dataset": os.getenv("BIGQUERY_DATASET", tfvars.get("bigquery_dataset_id", DEFAULT_DATASET)),
        "fact_table": os.getenv("BIGQUERY_FACT_TABLE", DEFAULT_FACT_TABLE),
        "city_dim_table": os.getenv("BIGQUERY_CITY_DIM_TABLE", DEFAULT_CITY_DIM_TABLE),
        "pollutant_dim_table": os.getenv("BIGQUERY_POLLUTANT_DIM_TABLE", DEFAULT_POLLUTANT_DIM_TABLE),
        "staging_table": os.getenv("BIGQUERY_STAGING_TABLE", DEFAULT_STAGING_TABLE),
        "location": os.getenv("BIGQUERY_LOCATION", tfvars.get("bigquery_location", DEFAULT_LOCATION)),
    }


def validate_resolved_args(args: argparse.Namespace) -> None:
    placeholder_args = {
        "--project-id": DEFAULT_PROJECT_ID,
        "--bucket": DEFAULT_BUCKET,
    }
    unresolved = [
        flag
        for flag, placeholder in placeholder_args.items()
        if getattr(args, flag.removeprefix("--").replace("-", "_")) == placeholder
    ]
    if unresolved:
        raise ValueError(
            "Warehouse loader still has placeholder configuration for "
            f"{', '.join(unresolved)}. Set environment variables, update terraform/terraform.tfvars, "
            "or pass explicit CLI arguments."
        )


def build_gcloud_env() -> dict[str, str]:
    env = os.environ.copy()
    if "CLOUDSDK_CONFIG" not in env and Path("/tmp/gcloud").exists():
        env["CLOUDSDK_CONFIG"] = "/tmp/gcloud"
    return env


def require_active_gcloud_account(env: dict[str, str]) -> None:
    result = subprocess.run(
        [
            "gcloud",
            "auth",
            "list",
            "--filter=status:ACTIVE",
            "--format=value(account)",
        ],
        check=False,
        text=True,
        capture_output=True,
        env=env,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise RuntimeError(stderr or "Unable to inspect active gcloud account.")
    if not result.stdout.strip():
        config_dir = env.get("CLOUDSDK_CONFIG", "")
        if config_dir:
            raise RuntimeError(
                "No active gcloud account selected for "
                f"CLOUDSDK_CONFIG={config_dir}. Run "
                f"`CLOUDSDK_CONFIG={config_dir} gcloud auth login` and "
                f"`CLOUDSDK_CONFIG={config_dir} gcloud config set project <project-id>` "
                "before loading BigQuery."
            )
        raise RuntimeError(
            "No active gcloud account selected. Run `gcloud auth login` "
            "and `gcloud config set project <project-id>` before loading BigQuery."
        )


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


def build_gcs_source_uris(silver_dir: Path, gcs_prefix: str) -> str:
    """Build a comma-separated list of exact partition URIs for bq load."""
    partition_dirs = sorted(
        {
            parquet_file.parent.relative_to(silver_dir).as_posix()
            for parquet_file in silver_dir.rglob("*.parquet")
        }
    )
    if not partition_dirs:
        raise FileNotFoundError(f"No Silver parquet files found in {silver_dir}")
    uris = [f"{gcs_prefix}/{partition_dir}/*.parquet" for partition_dir in partition_dirs]
    return ",".join(uris)


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
    defaults = build_defaults()
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", default=defaults["project_id"])
    parser.add_argument("--bucket", default=defaults["bucket"])
    parser.add_argument("--dataset", default=defaults["dataset"])
    parser.add_argument("--fact-table", default=defaults["fact_table"])
    parser.add_argument("--city-dim-table", default=defaults["city_dim_table"])
    parser.add_argument("--pollutant-dim-table", default=defaults["pollutant_dim_table"])
    parser.add_argument("--staging-table", default=defaults["staging_table"])
    parser.add_argument("--location", default=defaults["location"])
    args = parser.parse_args()
    validate_resolved_args(args)

    env = build_gcloud_env()

    try:
        require_active_gcloud_account(env)
        silver_dir = silver_dataset_path()
        gcs_prefix = f"gs://{args.bucket}/silver/air_quality_measurements"
        gcs_uri = build_gcs_source_uris(silver_dir, gcs_prefix)
        target_fq = f"{args.project_id}.{args.dataset}.{args.fact_table}"
        staging_fq = f"{args.project_id}.{args.dataset}.{args.staging_table}"
        staging_ref = f"{args.dataset}.{args.staging_table}"
        city_dim_fq = f"{args.project_id}.{args.dataset}.{args.city_dim_table}"
        pollutant_dim_fq = f"{args.project_id}.{args.dataset}.{args.pollutant_dim_table}"

        print(f"[INFO] Using Silver dataset: {silver_dir}")
        print(f"[INFO] Upload target: {gcs_prefix}")
        print(f"[INFO] BigQuery load source: {gcs_uri}")

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
                "--hive_partitioning_mode=AUTO",
                f"--hive_partitioning_source_uri_prefix={gcs_prefix}",
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
