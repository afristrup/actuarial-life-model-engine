from __future__ import annotations

import numpy as np
import polars as pl

from lifebook.portfolio_result import PortfolioResult


def profit_dataframe(result: PortfolioResult) -> pl.DataFrame:
    weight = result.arrays.weight
    pv_net = np.asarray(result.valuation.pv_net)
    net_cf = np.asarray(result.valuation.net_cashflow)

    weighted_pv_net = (pv_net * weight[:, None]).sum(axis=0)
    weighted_net_cf = (net_cf * weight[:, None]).sum(axis=0)
    t = np.arange(weighted_pv_net.shape[0])

    return pl.DataFrame(
        {
            "t": t,
            "net_cashflow": weighted_net_cf,
            "pv_net": weighted_pv_net,
            "cum_cashflow": np.cumsum(weighted_net_cf),
            "cum_profit": np.cumsum(weighted_pv_net),
        }
    )
