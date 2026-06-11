"""Speedup measurement: lifebook vs legacy model/ engine on the sample portfolio.

Not a correctness test — uses generous bounds so it won't false-positive on slow hardware.
The parity test in test_parity.py is the correctness check.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA = REPO_ROOT / "data"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.mark.benchmark
def test_lifebook_is_faster_than_legacy(capsys):
    from model.assumptions.assumption_loader import (
        load_expense_table as legacy_load_expense_table,
        load_lapse_table as legacy_load_lapse_table,
        load_mortality_parameters as legacy_load_mortality_parameters,
        load_mortality_table as legacy_load_mortality_table,
        load_yield_curve as legacy_load_yield_curve,
    )
    from model.assumptions.assumption_set import AssumptionSet
    from model.data.loader import load_portfolio_csv

    from lifebook import value_portfolio
    from lifebook.loaders.load_assumptions import load_assumptions
    from lifebook.loaders.load_portfolio import load_portfolio

    # Legacy
    legacy_mort = legacy_load_mortality_table(DATA / "mortality_tables" / "ons_mortality.csv")
    legacy_mort.mortality_parameters = legacy_load_mortality_parameters(
        DATA / "mortality_parameters" / "smoker_multipliers.csv"
    )
    legacy_assumptions = AssumptionSet(
        mortality=legacy_mort,
        interest=legacy_load_yield_curve(DATA / "yield_curves" / "sonia_spot_rates.csv"),
        lapse=legacy_load_lapse_table(DATA / "lapse_tables" / "lapse_rates.csv"),
        expenses=legacy_load_expense_table(DATA / "expense_tables" / "expense_rates.csv"),
    )
    legacy_portfolio = load_portfolio_csv(DATA / "portfolios" / "sample_portfolio.csv")

    t0 = time.perf_counter()
    legacy_portfolio.value(legacy_assumptions)
    legacy_seconds = time.perf_counter() - t0

    # lifebook (warm up jit first, since we're measuring steady-state)
    lifebook_assumptions = load_assumptions(
        mortality_path=DATA / "mortality_tables" / "ons_mortality.csv",
        yield_curve_path=DATA / "yield_curves" / "sonia_spot_rates.csv",
        smoker_multipliers_path=DATA / "mortality_parameters" / "smoker_multipliers.csv",
        lapse_path=DATA / "lapse_tables" / "lapse_rates.csv",
        expense_path=DATA / "expense_tables" / "expense_rates.csv",
    )
    lifebook_portfolio = load_portfolio(DATA / "portfolios" / "sample_portfolio.csv")
    _ = value_portfolio(lifebook_portfolio, lifebook_assumptions)  # warm jit

    t0 = time.perf_counter()
    r = value_portfolio(lifebook_portfolio, lifebook_assumptions)
    # force JAX to materialise arrays so we measure compute, not enqueue
    _ = float(r.totals.net_value)
    lifebook_seconds = time.perf_counter() - t0

    with capsys.disabled():
        print(
            f"\n  legacy:   {legacy_seconds * 1000:8.2f} ms"
            f"\n  lifebook: {lifebook_seconds * 1000:8.2f} ms"
            f"\n  speedup:  {legacy_seconds / lifebook_seconds:5.1f}x"
        )

    assert lifebook_seconds < legacy_seconds, (
        f"lifebook ({lifebook_seconds:.4f}s) should be faster than legacy "
        f"({legacy_seconds:.4f}s) after jit warmup"
    )
