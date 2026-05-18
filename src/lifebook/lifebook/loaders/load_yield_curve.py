from __future__ import annotations

from pathlib import Path

import polars as pl

from lifebook.models.yield_curve import YieldCurve

_REQUIRED = ("t", "spot_rate")


def load_yield_curve(path: str | Path) -> YieldCurve:
    raw = pl.read_csv(path)
    missing = [c for c in _REQUIRED if c not in raw.columns]
    if missing:
        raise ValueError(f"yield curve CSV missing columns: {missing}")

    df = raw.select(
        pl.col("t").cast(pl.Float64),
        (pl.col("spot_rate").cast(pl.Float64) / 100.0).alias("spot_rate"),
    )
    if df.null_count().sum_horizontal().item() > 0:
        raise ValueError("yield curve CSV has null values in required columns")
    if df.filter(pl.col("t") < 0).height > 0:
        raise ValueError("yield curve has negative maturity")
    if df.filter((pl.col("spot_rate") < 0) | (pl.col("spot_rate") > 1)).height > 0:
        raise ValueError("yield curve spot rate out of [0,1]")
    if df["t"].is_duplicated().any():
        raise ValueError("duplicate maturities in yield curve")

    spot_rates = dict(zip(df["t"].to_list(), df["spot_rate"].to_list(), strict=True))
    return YieldCurve(spot_rates=spot_rates)
