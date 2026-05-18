from __future__ import annotations

from pathlib import Path

import polars as pl

from lifebook.models.mortality_table import MortalityTable

_REQUIRED = ("gender", "age", "qx")


def load_mortality_table(path: str | Path) -> MortalityTable:
    raw = pl.read_csv(path)
    missing = [c for c in _REQUIRED if c not in raw.columns]
    if missing:
        raise ValueError(f"mortality CSV missing columns: {missing}")

    df = raw.select(
        pl.col("gender").cast(pl.Utf8),
        pl.col("age").cast(pl.Int64),
        pl.col("qx").cast(pl.Float64),
    )
    if df.null_count().sum_horizontal().item() > 0:
        raise ValueError("mortality CSV has null values in required columns")
    if df.filter(pl.col("age") < 0).height > 0:
        raise ValueError("mortality CSV has negative age")
    if df.filter((pl.col("qx") < 0) | (pl.col("qx") > 1)).height > 0:
        raise ValueError("mortality qx out of [0,1]")
    if df.select(["gender", "age"]).is_duplicated().any():
        raise ValueError("duplicate (gender, age) entries in mortality CSV")

    rates = {
        (g, int(a)): float(q)
        for g, a, q in zip(
            df["gender"].to_list(),
            df["age"].to_list(),
            df["qx"].to_list(),
            strict=True,
        )
    }
    return MortalityTable(rates=rates)
