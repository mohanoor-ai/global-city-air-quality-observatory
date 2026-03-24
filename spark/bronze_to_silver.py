"""Transform Bronze OpenAQ archives into a partitioned Silver parquet dataset."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
import csv
import json
import os
import sys

try:
    from pyspark.sql import DataFrame, SparkSession
    from pyspark.sql import functions as F
    from pyspark.sql import types as T
except ModuleNotFoundError:  # pragma: no cover - handled at runtime in main
    SparkSession = None  # type: ignore[assignment]
    DataFrame = object  # type: ignore[assignment]
    F = None  # type: ignore[assignment]
    T = None  # type: ignore[assignment]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ingestion.download_air_quality_data import (
    DEFAULT_TARGETS_FILE,
    scope_names,
    validate_scope_rows,
)


BRONZE_DIR = Path("data/bronze")
SILVER_DIR = Path("data/silver/air_quality_measurements")
METADATA_FILE = BRONZE_DIR / "location_metadata.csv"
RUN_SUMMARY_PATH = SILVER_DIR.parent / "latest_run_summary.json"
POLLUTANT_ALIASES = {"pm2.5": "pm25"}
ALLOWED_POLLUTANTS = ("pm25", "pm10", "no2", "co", "o3")


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--bronze-dir", default=str(BRONZE_DIR))
    parser.add_argument("--silver-dir", default=str(SILVER_DIR))
    parser.add_argument("--targets-file", default=str(DEFAULT_TARGETS_FILE))
    parser.add_argument("--write-mode", choices=["overwrite", "append"], default="overwrite")
    parser.add_argument(
        "--batch-date",
        default="",
        help="Optional YYYY-MM-DD batch date. Defaults to current UTC date in Spark.",
    )
    return parser.parse_args()


def load_scope_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            location_id = str(row.get("location_id", "")).strip()
            city = str(row.get("city", "")).strip()
            country = str(row.get("country", "")).strip().upper()
            if location_id and city and country:
                rows.append(
                    {
                        "location_id": location_id,
                        "city": city,
                        "country": country,
                    }
                )
    if not rows:
        raise ValueError(f"No scope metadata rows found in {path}")
    return rows


def scope_signature(rows: list[dict[str, str]]) -> set[tuple[str, str, str]]:
    return {
        (
            row["location_id"],
            row["city"].casefold(),
            row["country"].upper(),
        )
        for row in rows
    }


def load_scope_metadata(metadata_path: Path, targets_file: Path) -> list[dict[str, str]]:
    target_rows = load_scope_rows(targets_file)
    validate_scope_rows([(row["city"], row["country"]) for row in target_rows])

    if not metadata_path.exists():
        return target_rows

    metadata_rows = load_scope_rows(metadata_path)
    if scope_signature(metadata_rows) != scope_signature(target_rows):
        raise ValueError(
            f"Bronze metadata scope in {metadata_path} does not match {targets_file}. "
            "Rerun ingestion/download_air_quality_data.py to refresh Bronze metadata."
        )
    return metadata_rows


def build_spark() -> SparkSession:
    if SparkSession is None:
        raise ModuleNotFoundError(
            "pyspark is not installed. Install dependencies from requirements.txt first."
        )
    os.environ.pop("PYSPARK_DRIVER_PYTHON", None)
    os.environ.pop("PYSPARK_DRIVER_PYTHON_OPTS", None)
    os.environ.pop("PYSPARK_SUBMIT_ARGS", None)
    os.environ.pop("SPARK_HOME", None)
    os.environ["PYSPARK_PYTHON"] = sys.executable

    return (
        SparkSession.builder.appName("global-city-air-quality-observatory")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def bronze_schema() -> T.StructType:
    assert T is not None
    return T.StructType(
        [
            T.StructField("location_id", T.StringType(), True),
            T.StructField("sensors_id", T.StringType(), True),
            T.StructField("location", T.StringType(), True),
            T.StructField("datetime", T.StringType(), True),
            T.StructField("lat", T.DoubleType(), True),
            T.StructField("lon", T.DoubleType(), True),
            T.StructField("parameter", T.StringType(), True),
            T.StructField("units", T.StringType(), True),
            T.StructField("value", T.DoubleType(), True),
        ]
    )


def normalize_pollutant_name(name: str | None) -> str | None:
    if name is None:
        return None
    normalized = name.strip().lower()
    return POLLUTANT_ALIASES.get(normalized, normalized)


def build_silver_dataframe(
    spark: SparkSession,
    bronze_dir: Path,
    metadata_rows: list[dict[str, str]],
    batch_date: str,
) -> DataFrame:
    assert F is not None and T is not None
    bronze_df = (
        spark.read.option("header", True)
        .option("recursiveFileLookup", "true")
        .option("pathGlobFilter", "*.csv.gz")
        .schema(bronze_schema())
        .csv(str(bronze_dir))
        .withColumn("source_file", F.input_file_name())
    )

    metadata_schema = T.StructType(
        [
            T.StructField("location_id", T.StringType(), False),
            T.StructField("city", T.StringType(), False),
            T.StructField("country", T.StringType(), False),
        ]
    )
    metadata_df = spark.createDataFrame(metadata_rows, schema=metadata_schema)

    batch_date_column = F.lit(batch_date).cast("date") if batch_date else F.current_date()

    silver_df = (
        bronze_df.withColumn("pollutant", F.lower(F.trim(F.col("parameter"))))
        .replace(POLLUTANT_ALIASES, subset=["pollutant"])
        .withColumn(
            "measurement_datetime",
            F.to_timestamp("datetime", "yyyy-MM-dd'T'HH:mm:ssXXX"),
        )
        .withColumn("location_id", F.col("location_id").cast("long"))
        .withColumn("sensor_id", F.col("sensors_id").cast("long"))
        .withColumn("location_name", F.trim(F.col("location")))
        .withColumn("measurement_unit", F.trim(F.col("units")))
        .withColumn("measurement_value", F.col("value").cast("double"))
        .withColumnRenamed("lat", "latitude")
        .withColumnRenamed("lon", "longitude")
        .join(metadata_df.withColumn("location_id", F.col("location_id").cast("long")), on="location_id", how="inner")
        .filter(F.col("measurement_datetime").isNotNull())
        .filter(F.col("measurement_value").isNotNull())
        .filter(F.col("pollutant").isin(*ALLOWED_POLLUTANTS))
        .filter(F.col("city").isin(*scope_names()))
        .withColumn("measurement_date", F.to_date("measurement_datetime"))
        .withColumn("batch_date", batch_date_column)
        .select(
            "city",
            "country",
            "location_id",
            "location_name",
            "sensor_id",
            "pollutant",
            "measurement_value",
            "measurement_unit",
            "measurement_datetime",
            "measurement_date",
            "latitude",
            "longitude",
            "batch_date",
            "source_file",
        )
        .dropDuplicates(
            [
                "city",
                "location_id",
                "measurement_datetime",
                "pollutant",
                "measurement_value",
            ]
        )
    )
    return silver_df


def write_run_summary(df: DataFrame, silver_dir: Path, summary_path: Path) -> None:
    assert F is not None
    row = (
        df.agg(
            F.count("*").alias("row_count"),
            F.min("measurement_datetime").alias("min_timestamp"),
            F.max("measurement_datetime").alias("max_timestamp"),
        )
        .collect()[0]
    )
    city_counts = {
        item["city"]: item["count"]
        for item in df.groupBy("city").count().orderBy("city").collect()
    }
    summary = {
        "silver_dataset": str(silver_dir),
        "row_count": int(row["row_count"]),
        "city_counts": city_counts,
        "pollutants": list(ALLOWED_POLLUTANTS),
        "date_range": {
            "min": row["min_timestamp"].isoformat() if row["min_timestamp"] else None,
            "max": row["max_timestamp"].isoformat() if row["max_timestamp"] else None,
        },
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> int:
    args = parse_args()
    bronze_dir = Path(args.bronze_dir)
    silver_dir = Path(args.silver_dir)
    metadata_rows = load_scope_metadata(METADATA_FILE, Path(args.targets_file))

    if not bronze_dir.exists():
        raise FileNotFoundError(f"Bronze directory does not exist: {bronze_dir}")

    spark = build_spark()
    try:
        silver_df = build_silver_dataframe(
            spark=spark,
            bronze_dir=bronze_dir,
            metadata_rows=metadata_rows,
            batch_date=args.batch_date,
        )
        if silver_df.limit(1).count() == 0:
            raise ValueError("Spark transformation produced zero rows for the configured five-city scope.")

        silver_dir.mkdir(parents=True, exist_ok=True)
        (
            silver_df.repartition("batch_date")
            .write.mode(args.write_mode)
            .partitionBy("batch_date")
            .parquet(str(silver_dir))
        )
        write_run_summary(silver_df, silver_dir, RUN_SUMMARY_PATH)

        print(f"[PASS] Spark Silver dataset written to {silver_dir}")
        print(f"[INFO] Rows: {silver_df.count():,}")
        print(f"[INFO] Cities: {', '.join(scope_names())}")
        return 0
    finally:
        spark.stop()


if __name__ == "__main__":
    sys.exit(main())
