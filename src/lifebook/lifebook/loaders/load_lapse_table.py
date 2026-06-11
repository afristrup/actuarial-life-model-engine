from __future__ import annotations

from pathlib import Path

import polars as pl

from lifebook.models.lapse_segment import LapseSegment
from lifebook.models.lapse_table import LapseTable

_REQUIRED = ("product_type", "smoker_status", "duration_start", "duration_end", "lapse_rate")
_KEY_COLS = ["product_type", "smoker_status", "duration_start", "duration_end"]


def load_lapse_table(path: str | Path) -> LapseTable:
    raw = pl.read_csv(path)
    missing = [c for c in _REQUIRED if c not in raw.columns]
    if missing:
        raise ValueError(f"lapse CSV missing columns: {missing}")

    df = raw.select(
        pl.col("product_type").cast(pl.Utf8),
        pl.col("smoker_status").cast(pl.Utf8),
        pl.col("duration_start").cast(pl.Int64),
        pl.col("duration_end").cast(pl.Int64),
        pl.col("lapse_rate").cast(pl.Float64),
    )
    if df.null_count().sum_horizontal().item() > 0:
        raise ValueError("lapse CSV has null values in required columns")
    if df.filter(pl.col("duration_end") < pl.col("duration_start")).height > 0:
        raise ValueError("lapse CSV has duration_end < duration_start")
    if df.select(_KEY_COLS).is_duplicated().any():
        raise ValueError("duplicate lapse segments")
    _check_no_overlap(df)

    segments = tuple(LapseSegment.model_validate(row) for row in df.iter_rows(named=True))
    return LapseTable(segments=segments)


def _check_no_overlap(df: pl.DataFrame) -> None:
    overlap = (
        df.sort(["product_type", "smoker_status", "duration_start"])
        .with_columns(
            pl.col("duration_end")
            .shift(1)
            .over(["product_type", "smoker_status"])
            .alias("_prev_end")
        )
        .filter(pl.col("duration_start") <= pl.col("_prev_end"))
    )
    if overlap.height > 0:
        groups = overlap.select(["product_type", "smoker_status"]).unique().rows()
        raise ValueError(f"overlapping lapse ranges in {groups}")
