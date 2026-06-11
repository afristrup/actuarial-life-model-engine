from __future__ import annotations

import numpy as np
import polars as pl

from lifebook.models.expense_table import ExpenseTable
from lifebook.models.portfolio import Portfolio


def encode_expense(
    portfolio: Portfolio,
    expenses: ExpenseTable,
    t_max: int,
) -> tuple[np.ndarray, np.ndarray]:
    n = len(portfolio.policies)
    acquisition = np.zeros((n, t_max), dtype=np.float64)
    maintenance = np.zeros((n, t_max), dtype=np.float64)
    if not expenses.components or t_max == 0:
        return acquisition, maintenance

    comp_df = pl.DataFrame(
        {
            "expense_type": [c.expense_type for c in expenses.components],
            "amount_type": [c.amount_type for c in expenses.components],
            "value": [c.value for c in expenses.components],
            "comp_product": [c.product_type for c in expenses.components],
        }
    )
    pol_df = pl.DataFrame(
        {
            "i": list(range(n)),
            "product_type": [p.product_type for p in portfolio.policies],
            "premium": [p.premium for p in portfolio.policies],
            "term": [p.term for p in portfolio.policies],
        }
    )

    sums = (
        pol_df.join(comp_df, how="cross")
        .filter(
            pl.col("comp_product").is_null()
            | (pl.col("comp_product") == pl.col("product_type"))
        )
        .with_columns(
            amount=pl.when(pl.col("amount_type") == "fixed")
            .then(pl.col("value"))
            .otherwise(pl.col("value") * pl.col("premium"))
        )
        .group_by(["i", "expense_type"])
        .agg(pl.col("amount").sum())
    )

    acq_per_policy = _column_for(sums, pol_df, "acquisition")
    maint_per_policy = _column_for(sums, pol_df, "maintenance")

    acquisition[:, 0] = acq_per_policy
    term_arr = pol_df["term"].to_numpy()
    active = np.arange(t_max)[None, :] < term_arr[:, None]
    maintenance[:] = np.where(active, maint_per_policy[:, None], 0.0)

    return acquisition, maintenance


def _column_for(sums: pl.DataFrame, pol_df: pl.DataFrame, expense_type: str) -> np.ndarray:
    return (
        pol_df.select("i")
        .join(
            sums.filter(pl.col("expense_type") == expense_type).select("i", "amount"),
            on="i",
            how="left",
        )
        .sort("i")
        .with_columns(pl.col("amount").fill_null(0.0))["amount"]
        .to_numpy()
    )
