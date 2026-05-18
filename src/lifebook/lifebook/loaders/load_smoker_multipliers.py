from __future__ import annotations

from pathlib import Path

import polars as pl

from lifebook.models.smoker_multipliers import SmokerMultipliers

_REQUIRED = ("smoker_status", "mortality_multiplier")


def load_smoker_multipliers(path: str | Path) -> SmokerMultipliers:
    raw = pl.read_csv(path)
    missing = [c for c in _REQUIRED if c not in raw.columns]
    if missing:
        raise ValueError(f"smoker multipliers CSV missing columns: {missing}")

    df = raw.select(
        pl.col("smoker_status").cast(pl.Utf8),
        pl.col("mortality_multiplier").cast(pl.Float64),
    )
    if df.null_count().sum_horizontal().item() > 0:
        raise ValueError("smoker multipliers CSV has null values in required columns")
    if df.filter(pl.col("mortality_multiplier") < 0).height > 0:
        raise ValueError("smoker multipliers has negative value")
    if df["smoker_status"].is_duplicated().any():
        raise ValueError("duplicate smoker_status in smoker multipliers")

    multipliers = dict(
        zip(df["smoker_status"].to_list(), df["mortality_multiplier"].to_list(), strict=True)
    )
    return SmokerMultipliers(multipliers=multipliers)
