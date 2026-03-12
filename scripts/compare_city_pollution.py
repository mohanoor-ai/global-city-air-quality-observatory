"""Compare pollution metrics between two cities using Silver parquet data.

Example:
uv run python scripts/compare_city_pollution.py --city-a "Delhi" --city-b "London"
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


SILVER_DIR = Path("data/silver")


def latest_silver_file() -> Path:
    files = sorted(SILVER_DIR.glob("*.parquet"), key=lambda p: p.stat().st_mtime)
    if not files:
        raise FileNotFoundError(f"No Silver parquet files found in {SILVER_DIR}")
    return files[-1]


def city_stats(df: pd.DataFrame, city: str, pollutant: str) -> dict[str, object]:
    city_df = df[
        (df["city"].astype(str).str.lower() == city.lower())
        & (df["pollutant"].astype(str).str.lower() == pollutant.lower())
    ].copy()

    if city_df.empty:
        return {
            "city": city,
            "pollutant": pollutant,
            "measurement_count": 0,
            "avg_value": None,
            "max_value": None,
            "date_min": None,
            "date_max": None,
        }

    ts = pd.to_datetime(city_df["measurement_datetime"], errors="coerce", utc=True)
    return {
        "city": city,
        "pollutant": pollutant,
        "measurement_count": int(len(city_df)),
        "avg_value": float(city_df["value"].mean()),
        "max_value": float(city_df["value"].max()),
        "date_min": ts.min().isoformat() if not ts.dropna().empty else None,
        "date_max": ts.max().isoformat() if not ts.dropna().empty else None,
    }


def print_stats(stats: dict[str, object]) -> None:
    print(f"\nCity: {stats['city']}")
    print(f"Pollutant: {stats['pollutant']}")
    print(f"Measurements: {stats['measurement_count']}")
    if stats["measurement_count"] == 0:
        print("Average: n/a")
        print("Max: n/a")
        print("Date range: n/a")
        return
    print(f"Average: {stats['avg_value']:.3f}")
    print(f"Max: {stats['max_value']:.3f}")
    print(f"Date range: {stats['date_min']} -> {stats['date_max']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--city-a", required=True, help="First city to compare")
    parser.add_argument("--city-b", required=True, help="Second city to compare")
    parser.add_argument(
        "--pollutant",
        default="pm25",
        help="Pollutant to compare (default: pm25)",
    )
    parser.add_argument(
        "--silver-file",
        default="",
        help="Optional Silver parquet file path. Uses latest file if omitted.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    silver_path = Path(args.silver_file) if args.silver_file else latest_silver_file()
    if not silver_path.exists():
        raise FileNotFoundError(f"Missing Silver file: {silver_path}")

    print(f"[INFO] Using Silver file: {silver_path}")
    df = pd.read_parquet(silver_path)

    stats_a = city_stats(df, args.city_a, args.pollutant)
    stats_b = city_stats(df, args.city_b, args.pollutant)

    print_stats(stats_a)
    print_stats(stats_b)

    if stats_a["measurement_count"] and stats_b["measurement_count"]:
        delta = stats_a["avg_value"] - stats_b["avg_value"]  # type: ignore[operator]
        direction = "higher" if delta > 0 else "lower"
        print(
            f"\n[SUMMARY] {args.city_a} average {args.pollutant} is "
            f"{abs(delta):.3f} {direction} than {args.city_b}."
        )


if __name__ == "__main__":
    main()
