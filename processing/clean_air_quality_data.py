"""
Clean Bronze OpenAQ data and create the Silver dataset.

This script:
- reads Bronze csv.gz files one by one
- filters selected pollutants
- standardizes column names
- enriches rows with city and country metadata
- writes the cleaned dataset to Parquet
"""

import re
from pathlib import Path

import pandas as pd


BRONZE_DIR = Path("data/bronze")
SILVER_DIR = Path("data/silver")
METADATA_FILE = BRONZE_DIR / "location_metadata.csv"

POLLUTANTS = ["pm25", "pm10", "no2", "co", "o3"]
POLLUTANT_ALIASES = {"pm2.5": "pm25"}
SILVER_COLUMN_MAP = {
    "sensors_id": "sensor_id",
    "location": "location_name",
    "datetime": "measurement_datetime",
    "lat": "latitude",
    "lon": "longitude",
    "parameter": "pollutant",
    "units": "unit",
}


def load_location_metadata() -> pd.DataFrame:
    """Load location_id -> city/country mapping written during ingestion."""
    if not METADATA_FILE.exists():
        return pd.DataFrame(columns=["location_id", "city", "country"])

    metadata = pd.read_csv(METADATA_FILE)
    if metadata.empty:
        return pd.DataFrame(columns=["location_id", "city", "country"])

    metadata["location_id"] = pd.to_numeric(metadata["location_id"], errors="coerce")
    metadata = metadata.dropna(subset=["location_id"]).copy()
    metadata["location_id"] = metadata["location_id"].astype(int)
    metadata["city"] = metadata["city"].astype(str).str.strip()
    metadata["country"] = metadata["country"].astype(str).str.strip()
    return metadata[["location_id", "city", "country"]]


def build_output_path(df: pd.DataFrame, files: list[Path]) -> Path:
    """Create a descriptive Silver filename from input files + date range."""
    location_ids: set[str] = set()
    pattern = re.compile(r"location-(\d+)-\d{8}\.csv\.gz$")
    for path in files:
        match = pattern.search(path.name)
        if match:
            location_ids.add(match.group(1))

    if len(location_ids) == 1:
        location_part = f"location-{next(iter(location_ids))}"
    else:
        location_part = "multi-location"

    date_min = df["measurement_datetime"].min().strftime("%Y%m%d")
    date_max = df["measurement_datetime"].max().strftime("%Y%m%d")
    filename = f"air_quality_{location_part}_{date_min}_{date_max}.parquet"
    return SILVER_DIR / filename


def process_file(file_path: Path) -> pd.DataFrame:
    """Read one Bronze file and apply lightweight Silver cleaning rules."""
    df = pd.read_csv(file_path)

    # Normalize pollutant labels (OpenAQ may use pm2.5 instead of pm25).
    df["parameter"] = df["parameter"].astype(str).str.strip().str.lower()
    df["parameter"] = df["parameter"].replace(POLLUTANT_ALIASES)

    # Filter pollutants used in analysis.
    df = df[df["parameter"].isin(POLLUTANTS)].copy()

    # Rename columns to match Silver schema.
    df = df.rename(columns=SILVER_COLUMN_MAP)

    # Parse timestamp into a timezone-aware datetime.
    df["measurement_datetime"] = pd.to_datetime(
        df["measurement_datetime"],
        errors="coerce",
        utc=True,
    )

    return df


def main() -> None:
    # 1) Discover Bronze files.
    files = sorted(BRONZE_DIR.rglob("*.csv.gz"))
    if not files:
        raise FileNotFoundError(f"No files found in {BRONZE_DIR}")

    # 2) Process each file independently, then combine.
    cleaned_data: list[pd.DataFrame] = []
    for file_path in files:
        print(f"Processing {file_path}")
        cleaned_data.append(process_file(file_path))

    # 3) Build one Silver dataset, ordered by event time.
    final_df = pd.concat(cleaned_data, ignore_index=True)
    metadata_df = load_location_metadata()
    if not metadata_df.empty and "location_id" in final_df.columns:
        # Join city/country at location_id grain.
        final_df["location_id"] = pd.to_numeric(final_df["location_id"], errors="coerce")
        final_df = final_df.merge(metadata_df, on="location_id", how="left")
    else:
        final_df["city"] = pd.NA
        final_df["country"] = pd.NA

    # Keep a stable Silver schema even if metadata is missing.
    final_df["location_id"] = pd.to_numeric(final_df["location_id"], errors="coerce").astype("Int64")
    final_df["city"] = final_df["city"].fillna("unknown")
    final_df["country"] = final_df["country"].fillna("unknown")
    final_df = final_df.sort_values("measurement_datetime").reset_index(drop=True)
    final_df = final_df[
        [
            "measurement_datetime",
            "location_id",
            "location_name",
            "city",
            "country",
            "latitude",
            "longitude",
            "pollutant",
            "value",
            "unit",
            "sensor_id",
        ]
    ]

    # 4) Save using a descriptive filename for easy traceability.
    silver_path = build_output_path(final_df, files)
    silver_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_parquet(silver_path, index=False)

    print(f"[PASS] Silver dataset created: {silver_path}")
    print(f"[INFO] Rows: {len(final_df):,}")
    print(f"[INFO] Pollutants: {sorted(final_df['pollutant'].dropna().unique().tolist())}")
    print(
        f"[INFO] Date range: {final_df['measurement_datetime'].min()} -> "
        f"{final_df['measurement_datetime'].max()}"
    )


if __name__ == "__main__":
    main()
