"""
Download OpenAQ archive data and create the Bronze dataset.

This script:
- connects to the public OpenAQ AWS bucket
- lists csv.gz files for a target location and year
- downloads files one by one
- stores raw files in the Bronze layer
"""

from pathlib import Path
import boto3
from botocore import UNSIGNED
from botocore.config import Config

# AWS bucket configuration
BUCKET_NAME = "openaq-data-archive"
AWS_REGION = "us-east-1"

# London monitoring station
LOCATION_ID = "2178"

# Full year to download
YEAR = "2020"

# Local Bronze folder
LOCAL_PATH = Path("data/bronze/london")

# Create public S3 client
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    config=Config(signature_version=UNSIGNED),
)


def list_files(prefix):
    """List all csv.gz files from the selected S3 prefix."""
    paginator = s3.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]

            if key.endswith(".csv.gz"):
                yield key


def download_dataset():
    """Download all files for the selected London location and year."""
    prefix = f"records/csv.gz/locationid={LOCATION_ID}/year={YEAR}/"

    print("Downloading OpenAQ London yearly data")
    print(f"s3://{BUCKET_NAME}/{prefix}")
    print()

    downloaded = 0

    for key in list_files(prefix):
        filename = Path(key).name
        local_file = LOCAL_PATH / filename

        local_file.parent.mkdir(parents=True, exist_ok=True)

        print(f"Downloading: {key}")

        s3.download_file(
            BUCKET_NAME,
            key,
            str(local_file)
        )

        downloaded += 1

    print()
    print(f"Downloaded {downloaded} files.")


def main():
    download_dataset()


if __name__ == "__main__":
    main()
