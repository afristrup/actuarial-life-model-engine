from __future__ import annotations

import polars as pl

from lifebook import value_portfolio
from lifebook.analysis.profit_dataframe import profit_dataframe
from lifebook.models.assumptions import Assumptions
from lifebook.models.expense_component import ExpenseComponent
from lifebook.models.expense_table import ExpenseTable
from lifebook.models.mortality_table import MortalityTable
from lifebook.models.policy import Policy
from lifebook.models.portfolio import Portfolio
from lifebook.models.yield_curve import YieldCurve


def _trivial_setup() -> tuple[Portfolio, Assumptions]:
    portfolio = Portfolio(
        policies=(
            Policy(
                age=40, term=3, sum_assured=100_000.0, premium=500.0,
                gender="M", smoker_status="Smoker", product_type="Term", weight=2,
            ),
        )
    )
    assumptions = Assumptions(
        mortality=MortalityTable(rates={("M", a): 0.001 for a in (40, 41, 42)}),
        yield_curve=YieldCurve(spot_rates={1.0: 0.05, 2.0: 0.05, 3.0: 0.05}),
        expenses=ExpenseTable(
            components=(
                ExpenseComponent(expense_type="acquisition", amount_type="fixed", value=50.0),
                ExpenseComponent(expense_type="maintenance", amount_type="premium_pct", value=0.02),
            )
        ),
    )
    return portfolio, assumptions


def test_schema_and_length():
    portfolio, assumptions = _trivial_setup()
    df = profit_dataframe(value_portfolio(portfolio, assumptions))
    assert df.columns == ["t", "net_cashflow", "pv_net", "cum_cashflow", "cum_profit"]
    assert df.height == 3


def test_cum_profit_matches_aggregate_net_value():
    portfolio, assumptions = _trivial_setup()
    result = value_portfolio(portfolio, assumptions)
    df = profit_dataframe(result)
    last_cum = df.select(pl.col("cum_profit").last()).item()
    # cum_profit at the final period = total net value
    assert abs(last_cum - float(result.totals.net_value)) < 1e-9
