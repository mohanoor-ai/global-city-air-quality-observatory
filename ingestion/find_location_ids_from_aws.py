"""Find OpenAQ location IDs from the AWS archive using a city keyword.

This helper avoids API keys by scanning OpenAQ archive prefixes on S3.
It prints CSV-style lines:
location_id,location_name
"""

from __future__ import annotations

import argparse
import gzip
import io
import re

import boto3
import pandas as pd
from botocore import UNSIGNED
from botocore.config import Config


BUCKET_NAME = "openaq-data-archive"
ARCHIVE_PREFIX = "records/csv.gz/locationid="


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--keyword",
        required=True,
        help="City keyword to search in location names (example: delhi)",
    )
    parser.add_argument(
        "--max-matches",
        type=int,
        default=10,
        help="Maximum number of matches to print.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    keyword = args.keyword.strip().lower()
    if not keyword:
        raise ValueError("--keyword cannot be empty")

    s3 = boto3.client(
        "s3",
        region_name="us-east-1",
        config=Config(signature_version=UNSIGNED),
    )

    paginator = s3.get_paginator("list_objects_v2")
    matches = 0

    print("location_id,location_name")
    for page in paginator.paginate(
        Bucket=BUCKET_NAME,
        Prefix=ARCHIVE_PREFIX,
        Delimiter="/",
        PaginationConfig={"PageSize": 1000},
    ):
        for common_prefix in page.get("CommonPrefixes", []):
            prefix = common_prefix["Prefix"]
            location_match = re.search(r"locationid=(\d+)/", prefix)
            if not location_match:
                continue

            location_id = location_match.group(1)
            first_key_resp = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, MaxKeys=1)
            objects = first_key_resp.get("Contents", [])
            if not objects:
                continue

            key = objects[0]["Key"]
            try:
                body = s3.get_object(Bucket=BUCKET_NAME, Key=key)["Body"].read(150000)
                with gzip.GzipFile(fileobj=io.BytesIO(body)) as gz_file:
                    sample = pd.read_csv(gz_file, nrows=1)
            except Exception:
                continue

            location_name = str(sample.iloc[0].get("location", "")).strip()
            if keyword in location_name.lower():
                print(f"{location_id},{location_name}")
                matches += 1
                if matches >= args.max_matches:
                    return


if __name__ == "__main__":
    main()
