from __future__ import annotations

import numpy as np
import polars as pl

from lifebook.models.yield_curve import YieldCurve


def encode_discount(curve: YieldCurve, t_max: int) -> np.ndarray:
    rates = curve.spot_rates
    max_term = max(rates.keys())

    t_arr = np.arange(t_max, dtype=np.float64)
    lookup_keys = np.minimum(t_arr, max_term)

    lookup = pl.DataFrame(
        {"key": list(rates.keys()), "rate": list(rates.values())},
        schema={"key": pl.Float64, "rate": pl.Float64},
    )
    joined = pl.DataFrame({"key": lookup_keys}).join(lookup, on="key", how="left")

    missing = joined.with_row_index().filter(
        (pl.col("index") > 0) & pl.col("rate").is_null()
    )
    if missing.height > 0:
        raise ValueError(f"no spot rate for t={missing['key'].unique().to_list()}")

    rates_per_t = joined["rate"].fill_null(0.0).to_numpy().copy()
    rates_per_t[0] = 0.0
    return 1.0 / np.power(1.0 + rates_per_t, t_arr)
