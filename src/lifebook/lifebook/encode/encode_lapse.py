from __future__ import annotations

import numpy as np
import polars as pl

from lifebook.models.lapse_table import LapseTable
from lifebook.models.portfolio import Portfolio


def encode_lapse(
    portfolio: Portfolio,
    lapse: LapseTable,
    t_max: int,
) -> np.ndarray:
    n = len(portfolio.policies)
    out = np.zeros((n, t_max), dtype=np.float64)
    if not lapse.segments or t_max == 0:
        return out

    segments_df = pl.DataFrame(
        {
            "product_type": [s.product_type for s in lapse.segments],
            "smoker_status": [s.smoker_status for s in lapse.segments],
            "duration_start": [s.duration_start for s in lapse.segments],
            "duration_end": [s.duration_end for s in lapse.segments],
            "lapse_rate": [s.lapse_rate for s in lapse.segments],
        }
    )

    policies_df = pl.DataFrame(
        {
            "i": list(range(n)),
            "product_type": [p.product_type for p in portfolio.policies],
            "smoker_status": [p.smoker_status for p in portfolio.policies],
            "term": [p.term for p in portfolio.policies],
        }
    )

    durations_df = pl.DataFrame(
        {"t": list(range(t_max)), "duration": list(range(1, t_max + 1))}
    )

    matched = (
        policies_df.join(durations_df, how="cross")
        .filter(pl.col("t") < pl.col("term"))
        .join(segments_df, on=["product_type", "smoker_status"], how="inner")
        .filter(
            (pl.col("duration_start") <= pl.col("duration"))
            & (pl.col("duration") <= pl.col("duration_end"))
        )
        .select("i", "t", "lapse_rate")
    )

    if matched.height > 0:
        out[matched["i"].to_numpy(), matched["t"].to_numpy()] = matched[
            "lapse_rate"
        ].to_numpy()
    return out
