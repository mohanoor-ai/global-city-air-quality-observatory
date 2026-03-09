"""
Air Quality Data Ingestion

This script downloads the latest PM2.5 air quality measurements
from the OpenAQ API v3 and stores them locally as a Parquet file.

Why this approach:
- OpenAQ API v2 is retired
- v3 provides a /parameters/{id}/latest endpoint
- this gives us a simple and stable starting point for the pipeline
"""

from pathlib import Path

import pandas as pd
import requests


API_URL = "https://api.openaq.org/v3/parameters/2/latest"
OUTPUT_DIR = Path("data/raw")
OUTPUT_FILE = OUTPUT_DIR / "air_quality_raw.parquet"


def fetch_latest_air_quality(limit: int = 1000, page: int = 1) -> list[dict]:
    """
    Fetch the latest PM2.5 measurements from OpenAQ API v3.

    Args:
        limit: Number of records to request
        page: Page number

    Returns:
        List of measurement records
    """
    params = {
        "limit": limit,
        "page": page,
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    payload = response.json()
    return payload.get("results", [])


def normalize_results(results: list[dict]) -> pd.DataFrame:
    """
    Convert nested JSON results into a flat pandas DataFrame.
    """
    df = pd.json_normalize(results)

    # Optional: rename a few important columns to make them clearer
    rename_map = {
        "datetime.utc": "measurement_datetime_utc",
        "datetime.local": "measurement_datetime_local",
        "coordinates.latitude": "latitude",
        "coordinates.longitude": "longitude",
        "locationsId": "location_id",
        "sensorsId": "sensor_id",
    }

    df = df.rename(columns=rename_map)

    return df


def save_to_parquet(df: pd.DataFrame) -> None:
    """
    Save the DataFrame to the raw data folder as Parquet.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_FILE, index=False)
    print(f"Raw data saved to: {OUTPUT_FILE}")


def main() -> None:
    print("Downloading latest PM2.5 air quality data from OpenAQ v3...")

    results = fetch_latest_air_quality(limit=1000, page=1)

    if not results:
        print("No data returned from the API.")
        return

    df = normalize_results(results)

    print(f"Downloaded {len(df)} records")
    print("Saving dataset as Parquet...")

    save_to_parquet(df)

    print("Ingestion completed successfully.")


if __name__ == "__main__":
    main()