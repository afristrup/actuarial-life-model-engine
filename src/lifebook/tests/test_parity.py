"""Parity smoke test: lifebook must match legacy model/ engine on real portfolio data."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA = REPO_ROOT / "data"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture(scope="module")
def legacy_total() -> dict:
    """Run the legacy model/ engine end-to-end and return totals."""
    from model.assumptions.assumption_loader import (
        load_expense_table,
        load_lapse_table,
        load_mortality_parameters,
        load_mortality_table,
        load_yield_curve,
    )
    from model.assumptions.assumption_set import AssumptionSet
    from model.data.loader import load_portfolio_csv

    mortality_params = load_mortality_parameters(DATA / "mortality_parameters" / "smoker_multipliers.csv")
    mortality_table = load_mortality_table(DATA / "mortality_tables" / "ons_mortality.csv")
    mortality_table.mortality_parameters = mortality_params
    yield_curve = load_yield_curve(DATA / "yield_curves" / "sonia_spot_rates.csv")
    lapse = load_lapse_table(DATA / "lapse_tables" / "lapse_rates.csv")
    expenses = load_expense_table(DATA / "expense_tables" / "expense_rates.csv")

    assumptions = AssumptionSet(
        mortality=mortality_table,
        interest=yield_curve,
        lapse=lapse,
        expenses=expenses,
    )

    portfolio = load_portfolio_csv(DATA / "portfolios" / "sample_portfolio.csv")
    result = portfolio.value(assumptions, return_breakdown=False)
    return {
        "pv_premiums": result.pv_premiums,
        "pv_claims": result.pv_claims,
        "pv_expenses": result.pv_expenses,
        "net_value": result.net_value,
        "policy_count": result.policy_count,
    }


@pytest.fixture(scope="module")
def lifebook_total() -> dict:
    from lifebook import value_portfolio
    from lifebook.loaders.load_assumptions import load_assumptions
    from lifebook.loaders.load_portfolio import load_portfolio

    assumptions = load_assumptions(
        mortality_path=DATA / "mortality_tables" / "ons_mortality.csv",
        yield_curve_path=DATA / "yield_curves" / "sonia_spot_rates.csv",
        smoker_multipliers_path=DATA / "mortality_parameters" / "smoker_multipliers.csv",
        lapse_path=DATA / "lapse_tables" / "lapse_rates.csv",
        expense_path=DATA / "expense_tables" / "expense_rates.csv",
    )
    portfolio = load_portfolio(DATA / "portfolios" / "sample_portfolio.csv")
    result = value_portfolio(portfolio, assumptions)
    t = result.totals
    return {
        "pv_premiums": float(t.pv_premiums),
        "pv_claims": float(t.pv_claims),
        "pv_expenses": float(t.pv_expenses),
        "net_value": float(t.net_value),
        "policy_count": result.policy_count,
    }


def test_policy_count(legacy_total, lifebook_total):
    assert legacy_total["policy_count"] == lifebook_total["policy_count"]


@pytest.mark.parametrize("key", ["pv_premiums", "pv_claims", "pv_expenses", "net_value"])
def test_totals_match(legacy_total, lifebook_total, key):
    np.testing.assert_allclose(
        lifebook_total[key],
        legacy_total[key],
        rtol=1e-9,
        atol=1e-3,
        err_msg=f"{key}: legacy={legacy_total[key]}, lifebook={lifebook_total[key]}",
    )
