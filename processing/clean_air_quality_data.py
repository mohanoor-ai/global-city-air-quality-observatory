"""
Clean Bronze OpenAQ data and create the Silver dataset.

This script:
- reads Bronze csv.gz files one by one
- filters selected pollutants
- standardizes column names
- writes the cleaned dataset to Parquet
"""

from pathlib import Path
import re

import pandas as pd


BRONZE_DIR = Path("data/bronze/london")
SILVER_DIR = Path("data/silver")

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
    files = sorted(BRONZE_DIR.glob("*.csv.gz"))
    if not files:
        raise FileNotFoundError(f"No files found in {BRONZE_DIR}")

    # 2) Process each file independently, then combine.
    cleaned_data: list[pd.DataFrame] = []
    for file_path in files:
        print(f"Processing {file_path}")
        cleaned_data.append(process_file(file_path))

    # 3) Build one Silver dataset, ordered by event time.
    final_df = pd.concat(cleaned_data, ignore_index=True)
    final_df = final_df.sort_values("measurement_datetime").reset_index(drop=True)

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
