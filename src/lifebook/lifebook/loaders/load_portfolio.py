from __future__ import annotations

from pathlib import Path

import polars as pl

from lifebook.models.policy import Policy
from lifebook.models.portfolio import Portfolio

_REQUIRED = ("age", "term", "sum_assured", "premium")
_POLICY_COLS = (
    "age",
    "term",
    "sum_assured",
    "premium",
    "gender",
    "smoker_status",
    "product_type",
    "weight",
    "policy_id",
)


def load_portfolio(path: str | Path) -> Portfolio:
    raw = pl.read_csv(path)
    missing = [c for c in _REQUIRED if c not in raw.columns]
    if missing:
        raise ValueError(f"portfolio CSV missing columns: {missing}")

    df = raw.with_columns(
        pl.col("age").cast(pl.Int64),
        pl.col("term").cast(pl.Int64),
        pl.col("sum_assured").cast(pl.Float64),
        pl.col("premium").cast(pl.Float64),
    )
    if df.select(_REQUIRED).null_count().sum_horizontal().item() > 0:
        raise ValueError("portfolio CSV has null values in required columns")

    keep = [c for c in _POLICY_COLS if c in df.columns]
    policies = tuple(
        Policy.model_validate(row) for row in df.select(keep).iter_rows(named=True)
    )
    return Portfolio(policies=policies)
