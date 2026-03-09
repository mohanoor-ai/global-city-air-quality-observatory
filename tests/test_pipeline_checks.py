import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from processing import check_silver_data_quality as dq
from processing import clean_air_quality_data as clean


class TestProcessing(unittest.TestCase):
    def test_process_file_filters_and_normalizes_pollutants(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "sample.csv"
            df = pd.DataFrame(
                [
                    {
                        "location_id": 1,
                        "sensors_id": 100,
                        "location": "Test Station",
                        "datetime": "2020-01-01T00:00:00+00:00",
                        "lat": 51.5,
                        "lon": -0.1,
                        "parameter": "pm2.5",
                        "units": "ug/m3",
                        "value": 10.0,
                    },
                    {
                        "location_id": 1,
                        "sensors_id": 100,
                        "location": "Test Station",
                        "datetime": "2020-01-01T01:00:00+00:00",
                        "lat": 51.5,
                        "lon": -0.1,
                        "parameter": "no2",
                        "units": "ug/m3",
                        "value": 20.0,
                    },
                    {
                        "location_id": 1,
                        "sensors_id": 100,
                        "location": "Test Station",
                        "datetime": "2020-01-01T02:00:00+00:00",
                        "lat": 51.5,
                        "lon": -0.1,
                        "parameter": "so2",
                        "units": "ug/m3",
                        "value": 30.0,
                    },
                ]
            )
            df.to_csv(csv_path, index=False)

            result = clean.process_file(csv_path)

            self.assertEqual(set(result["pollutant"].unique().tolist()), {"pm25", "no2"})
            self.assertNotIn("so2", result["pollutant"].unique().tolist())
            self.assertIn("measurement_datetime", result.columns)
            self.assertIn("location_name", result.columns)


class TestDataQuality(unittest.TestCase):
    def test_dq_pass_writes_json_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            silver_dir = Path(tmp) / "silver"
            quality_dir = Path(tmp) / "quality"
            silver_dir.mkdir(parents=True, exist_ok=True)
            quality_dir.mkdir(parents=True, exist_ok=True)

            silver_file = silver_dir / "air_quality_location-1_20200101_20200101.parquet"
            pd.DataFrame(
                [
                    {
                        "measurement_datetime": "2020-01-01T00:00:00+00:00",
                        "location_name": "Test Station",
                        "latitude": 51.5,
                        "longitude": -0.1,
                        "pollutant": "pm25",
                        "value": 10.0,
                        "unit": "ug/m3",
                    }
                ]
            ).to_parquet(silver_file, index=False)

            with (
                patch.object(dq, "SILVER_DIR", silver_dir),
                patch.object(dq, "QUALITY_DIR", quality_dir),
                patch("sys.argv", ["check_silver_data_quality.py"]),
            ):
                exit_code = dq.main()

            self.assertEqual(exit_code, 0)
            report_path = quality_dir / f"{silver_file.stem}_dq_report.json"
            self.assertTrue(report_path.exists())
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "pass")
            self.assertEqual(report["row_count"], 1)

    def test_dq_fails_when_no_silver_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            silver_dir = Path(tmp) / "silver"
            quality_dir = Path(tmp) / "quality"
            silver_dir.mkdir(parents=True, exist_ok=True)
            quality_dir.mkdir(parents=True, exist_ok=True)

            with (
                patch.object(dq, "SILVER_DIR", silver_dir),
                patch.object(dq, "QUALITY_DIR", quality_dir),
                patch("sys.argv", ["check_silver_data_quality.py"]),
            ):
                exit_code = dq.main()

            self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
