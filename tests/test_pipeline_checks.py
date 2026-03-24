import json
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from ingestion import city_scope
from ingestion import download_air_quality_data as ingest
from spark import bronze_to_silver as spark_transform
from spark import check_silver_data_quality as dq


class TestSparkHelpers(unittest.TestCase):
    def test_normalize_pollutant_name_handles_pm25_alias(self) -> None:
        self.assertEqual(spark_transform.normalize_pollutant_name("pm2.5"), "pm25")
        self.assertEqual(spark_transform.normalize_pollutant_name("NO2"), "no2")

    def test_load_scope_metadata_reads_targets_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            targets_file = Path(tmp) / "location_targets.csv"
            targets_file.write_text(
                "location_id,city,country\n159,London,GB\n2451,New York,US\n8118,Delhi,IN\n1451,Beijing,CN\n3019,Berlin,DE\n",
                encoding="utf-8",
            )

            rows = spark_transform.load_scope_metadata(Path(tmp) / "missing.csv", targets_file)

            self.assertEqual(len(rows), 5)
            self.assertEqual(rows[0]["city"], "London")


class TestDataQuality(unittest.TestCase):
    def test_dq_pass_writes_json_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            silver_dir = Path(tmp) / "air_quality_measurements" / "batch_date=2026-03-13"
            report_path = Path(tmp) / "quality" / "silver_dq_report.json"
            silver_dir.mkdir(parents=True, exist_ok=True)

            silver_file = silver_dir / "part-0000.parquet"
            pd.DataFrame(
                [
                    {
                        "city": "London",
                        "country": "GB",
                        "location_id": 159,
                        "location_name": "London Station",
                        "pollutant": "pm25",
                        "measurement_value": 10.0,
                        "measurement_unit": "ug/m3",
                        "measurement_datetime": "2020-01-01T00:00:00+00:00",
                        "measurement_date": "2020-01-01",
                        "latitude": 51.5,
                        "longitude": -0.1,
                        "source_file": "sample.csv.gz",
                    },
                    {
                        "city": "New York",
                        "country": "US",
                        "location_id": 2451,
                        "location_name": "NYC Station",
                        "pollutant": "pm25",
                        "measurement_value": 12.0,
                        "measurement_unit": "ug/m3",
                        "measurement_datetime": "2020-01-01T00:00:00+00:00",
                        "measurement_date": "2020-01-01",
                        "latitude": 40.7,
                        "longitude": -74.0,
                        "source_file": "sample.csv.gz",
                    },
                    {
                        "city": "Delhi",
                        "country": "IN",
                        "location_id": 8118,
                        "location_name": "Delhi Station",
                        "pollutant": "pm10",
                        "measurement_value": 30.0,
                        "measurement_unit": "ug/m3",
                        "measurement_datetime": "2020-01-01T00:00:00+00:00",
                        "measurement_date": "2020-01-01",
                        "latitude": 28.6,
                        "longitude": 77.2,
                        "source_file": "sample.csv.gz",
                    },
                    {
                        "city": "Beijing",
                        "country": "CN",
                        "location_id": 1451,
                        "location_name": "Beijing Station",
                        "pollutant": "no2",
                        "measurement_value": 15.0,
                        "measurement_unit": "ug/m3",
                        "measurement_datetime": "2020-01-01T00:00:00+00:00",
                        "measurement_date": "2020-01-01",
                        "latitude": 39.9,
                        "longitude": 116.4,
                        "source_file": "sample.csv.gz",
                    },
                    {
                        "city": "Berlin",
                        "country": "DE",
                        "location_id": 3019,
                        "location_name": "Berlin Station",
                        "pollutant": "o3",
                        "measurement_value": 9.0,
                        "measurement_unit": "ug/m3",
                        "measurement_datetime": "2020-01-01T00:00:00+00:00",
                        "measurement_date": "2020-01-01",
                        "latitude": 52.52,
                        "longitude": 13.405,
                        "source_file": "sample.csv.gz",
                    },
                ]
            ).to_parquet(silver_file, index=False)

            with patch("sys.argv", ["check_silver_data_quality.py", "--silver-dir", str(silver_dir.parent), "--report-path", str(report_path)]):
                exit_code = dq.main()

            self.assertEqual(exit_code, 0)
            self.assertTrue(report_path.exists())
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "pass")
            self.assertEqual(report["row_count"], 5)

    def test_dq_fails_when_no_silver_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            silver_dir = Path(tmp) / "air_quality_measurements"
            report_path = Path(tmp) / "quality" / "silver_dq_report.json"
            silver_dir.mkdir(parents=True, exist_ok=True)

            with patch("sys.argv", ["check_silver_data_quality.py", "--silver-dir", str(silver_dir), "--report-path", str(report_path)]):
                exit_code = dq.main()

            self.assertEqual(exit_code, 1)


class TestIngestion(unittest.TestCase):
    def test_load_targets_reads_location_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            targets_file = Path(tmp) / "location_targets.csv"
            targets_file.write_text(
                "location_id,city,country\n159,London,GB\n2451,New York,US\n8118,Delhi,IN\n1451,Beijing,CN\n3019,Berlin,DE\n",
                encoding="utf-8",
            )

            targets = ingest.load_targets(targets_file)

            self.assertEqual(len(targets), 5)
            self.assertEqual(targets[0].location_id, "159")
            self.assertEqual(targets[-1].city, "Berlin")

    def test_load_scope_metadata_rejects_stale_bronze_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            targets_file = Path(tmp) / "location_targets.csv"
            metadata_file = Path(tmp) / "location_metadata.csv"
            targets_file.write_text(
                "location_id,city,country\n159,London,GB\n2451,New York,US\n8118,Delhi,IN\n1451,Beijing,CN\n3019,Berlin,DE\n",
                encoding="utf-8",
            )
            metadata_file.write_text(
                "location_id,city,country\n159,London,GB\n2451,New York,US\n8118,Delhi,IN\n1451,Beijing,CN\n9999,Berlin,DE\n",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                spark_transform.load_scope_metadata(metadata_file, targets_file)

    def test_backfill_months_last_two_full_years_plus_ytd(self) -> None:
        now = datetime(2026, 3, 10, tzinfo=UTC)
        periods = ingest.backfill_months(now)

        self.assertEqual(periods[0], (2024, 1))
        self.assertEqual(periods[-1], (2026, 3))
        self.assertEqual(len(periods), 27)

    def test_city_scope_validation_requires_exact_five_city_list(self) -> None:
        with self.assertRaises(ValueError):
            city_scope.validate_scope_rows([("London", "GB")])


class TestIngestionVerification(unittest.TestCase):
    def test_verify_bronze_fails_when_a_configured_location_has_no_raw_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            targets_file = Path(tmp) / "location_targets.csv"
            bronze_dir = Path(tmp) / "bronze"
            metadata_file = bronze_dir / "location_metadata.csv"
            location_dir = bronze_dir / "records" / "csv.gz" / "locationid=159" / "year=2026" / "month=03"
            scope_csv = (
                "location_id,city,country\n"
                "159,London,GB\n"
                "2451,New York,US\n"
                "8118,Delhi,IN\n"
                "1451,Beijing,CN\n"
                "3019,Berlin,DE\n"
            )

            targets_file.write_text(scope_csv, encoding="utf-8")
            metadata_file.parent.mkdir(parents=True, exist_ok=True)
            metadata_file.write_text(scope_csv, encoding="utf-8")
            location_dir.mkdir(parents=True, exist_ok=True)
            (location_dir / "location-159-20260301.csv.gz").write_text("sample", encoding="utf-8")
            targets = ingest.load_targets(targets_file)
            exit_code = ingest.verify_bronze(
                targets,
                bronze_dir=bronze_dir,
                metadata_file=metadata_file,
            )

            self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
