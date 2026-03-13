"""Fixed five-city analytical scope used across ingestion, Spark, and docs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_TARGETS_FILE = Path("ingestion/location_targets.csv")


@dataclass(frozen=True)
class ScopedCity:
    city: str
    country: str
    rationale: str


CITY_SCOPE: tuple[ScopedCity, ...] = (
    ScopedCity(
        city="London",
        country="GB",
        rationale="European reference city with mature monitoring coverage and lower baseline PM2.5.",
    ),
    ScopedCity(
        city="New York",
        country="US",
        rationale="North American comparison city with dense monitoring and a different emissions mix.",
    ),
    ScopedCity(
        city="Delhi",
        country="IN",
        rationale="High-pollution South Asian city that creates strong analytical contrast.",
    ),
    ScopedCity(
        city="Beijing",
        country="CN",
        rationale="East Asian megacity with notable policy-driven shifts in pollutant patterns.",
    ),
    ScopedCity(
        city="São Paulo",
        country="BR",
        rationale="South American city that broadens geographic coverage while keeping the dashboard readable.",
    ),
)


def scope_pairs() -> set[tuple[str, str]]:
    return {(item.city.casefold(), item.country.upper()) for item in CITY_SCOPE}


def scope_names() -> list[str]:
    return [item.city for item in CITY_SCOPE]


def validate_scope_rows(rows: list[tuple[str, str]]) -> None:
    expected = scope_pairs()
    actual = {(city.casefold(), country.upper()) for city, country in rows}
    if len(rows) != len(CITY_SCOPE):
        raise ValueError(
            f"Expected exactly {len(CITY_SCOPE)} configured cities, found {len(rows)}."
        )
    if actual != expected:
        raise ValueError(
            "Configured city scope does not match the fixed project scope: "
            f"{scope_names()}."
        )
