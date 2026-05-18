from __future__ import annotations

import numpy as np
import polars as pl


def engineer(
    df: pl.DataFrame,
    expressions: list[pl.Expr],
    target: str,
) -> tuple[np.ndarray, np.ndarray]:
    if target not in df.columns:
        raise ValueError(f"target {target!r} not in columns {df.columns}")

    out = df.with_columns(expressions).drop_nulls()
    if out.height == 0:
        raise ValueError("no rows remain after drop_nulls")

    feature_cols = [c for c in out.columns if c != target]
    if not feature_cols:
        raise ValueError("no feature columns after excluding target")

    X = out.select(feature_cols).to_numpy()
    y = out.select(target).to_numpy().ravel()
    return X, y
