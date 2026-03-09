"""
Air Quality Data Ingestion

This script downloads air quality measurements from the OpenAQ API
and stores them locally as a Parquet file.

This represents the raw ingestion stage of the pipeline.
"""

import requests
import pandas as pd
from pathlib import Path


API_URL = "https://api.openaq.org/v2/measurements"


def fetch_air_quality_data(limit=1000, pages=5):
    """
    Fetch air quality data from the OpenAQ API using pagination.
    """

    all_results = []

    for page in range(1, pages + 1):

        params = {
            "limit": limit,
            "page": page
        }

        print(f"Fetching page {page}...")

        response = requests.get(API_URL, params=params)
        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            break

        all_results.extend(results)

    return all_results


def transform_to_dataframe(results):
    """
    Convert JSON results into a pandas DataFrame.
    """

    df = pd.json_normalize(results)

    return df


def save_raw_parquet(df):
    """
    Save dataset as Parquet file in raw layer.
    """

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "air_quality_raw.parquet"

    df.to_parquet(output_file, index=False)

    print(f"Raw data saved to {output_file}")


def main():

    print("Starting air quality data ingestion...")

    results = fetch_air_quality_data()

    print(f"Records downloaded: {len(results)}")

    df = transform_to_dataframe(results)

    print("Saving dataset...")

    save_raw_parquet(df)

    print("Ingestion completed successfully.")


if __name__ == "__main__":
    main()