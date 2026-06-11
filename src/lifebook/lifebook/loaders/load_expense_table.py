from __future__ import annotations

from pathlib import Path

import polars as pl

from lifebook.models.expense_component import ExpenseComponent
from lifebook.models.expense_table import ExpenseTable

_REQUIRED = ("expense_type", "amount_type", "value")
_ALLOWED_EXPENSE_TYPES = ("acquisition", "maintenance")
_ALLOWED_AMOUNT_TYPES = ("fixed", "premium_pct")


def load_expense_table(path: str | Path) -> ExpenseTable:
    raw = pl.read_csv(path)
    missing = [c for c in _REQUIRED if c not in raw.columns]
    if missing:
        raise ValueError(f"expense CSV missing columns: {missing}")

    df = raw.with_columns(pl.col("value").cast(pl.Float64))
    if df.select(_REQUIRED).null_count().sum_horizontal().item() > 0:
        raise ValueError("expense CSV has null values in required columns")
    if df.filter(pl.col("value") < 0).height > 0:
        raise ValueError("expense CSV has negative value")
    bad_expense = df.filter(~pl.col("expense_type").is_in(_ALLOWED_EXPENSE_TYPES))
    if bad_expense.height > 0:
        raise ValueError(
            f"expense_type must be one of {_ALLOWED_EXPENSE_TYPES}; got {bad_expense['expense_type'].unique().to_list()}"
        )
    bad_amount = df.filter(~pl.col("amount_type").is_in(_ALLOWED_AMOUNT_TYPES))
    if bad_amount.height > 0:
        raise ValueError(
            f"amount_type must be one of {_ALLOWED_AMOUNT_TYPES}; got {bad_amount['amount_type'].unique().to_list()}"
        )

    components = tuple(
        ExpenseComponent.model_validate(row) for row in df.iter_rows(named=True)
    )
    return ExpenseTable(components=components)
