from __future__ import annotations

from typing import NamedTuple

import numpy as np
import polars as pl

from lifebook.models.portfolio import Portfolio


class PortfolioArrays(NamedTuple):
    age: np.ndarray
    term: np.ndarray
    sum_assured: np.ndarray
    premium: np.ndarray
    weight: np.ndarray


def encode_portfolio(portfolio: Portfolio) -> PortfolioArrays:
    df = pl.DataFrame(portfolio.model_dump()["policies"])
    return PortfolioArrays(
        age=df["age"].to_numpy().astype(np.int32),
        term=df["term"].to_numpy().astype(np.int32),
        sum_assured=df["sum_assured"].to_numpy().astype(np.float64),
        premium=df["premium"].to_numpy().astype(np.float64),
        weight=df["weight"].to_numpy().astype(np.float64),
    )
