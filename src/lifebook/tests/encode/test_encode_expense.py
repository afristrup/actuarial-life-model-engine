from __future__ import annotations

import numpy as np

from lifebook.encode.encode_expense import encode_expense
from lifebook.models.expense_component import ExpenseComponent
from lifebook.models.expense_table import ExpenseTable
from lifebook.models.policy import Policy
from lifebook.models.portfolio import Portfolio


def _policy(**overrides) -> Policy:
    base = dict(
        age=40, term=3, sum_assured=100_000.0, premium=500.0,
        gender="M", smoker_status="Smoker", product_type="Term", weight=1,
    )
    base.update(overrides)
    return Policy(**base)


def test_acquisition_at_t0_only():
    portfolio = Portfolio(policies=(_policy(),))
    table = ExpenseTable(
        components=(ExpenseComponent(expense_type="acquisition", amount_type="fixed", value=40.0),)
    )
    acq, maint = encode_expense(portfolio, table, t_max=3)
    np.testing.assert_array_equal(acq, [[40.0, 0.0, 0.0]])
    np.testing.assert_array_equal(maint, [[0.0, 0.0, 0.0]])


def test_maintenance_is_constant_within_term():
    portfolio = Portfolio(policies=(_policy(term=2, premium=1000.0),))
    table = ExpenseTable(
        components=(ExpenseComponent(expense_type="maintenance", amount_type="premium_pct", value=0.02),)
    )
    acq, maint = encode_expense(portfolio, table, t_max=4)
    np.testing.assert_array_equal(acq, [[0.0, 0.0, 0.0, 0.0]])
    np.testing.assert_array_equal(maint, [[20.0, 20.0, 0.0, 0.0]])


def test_premium_pct_uses_policy_premium():
    portfolio = Portfolio(policies=(_policy(premium=200.0),))
    table = ExpenseTable(
        components=(ExpenseComponent(expense_type="acquisition", amount_type="premium_pct", value=0.1),)
    )
    acq, _ = encode_expense(portfolio, table, t_max=3)
    assert acq[0, 0] == 20.0


def test_product_type_filter():
    portfolio = Portfolio(policies=(_policy(product_type="Term"), _policy(product_type="Endowment")))
    table = ExpenseTable(
        components=(
            ExpenseComponent(
                expense_type="acquisition", amount_type="fixed", value=100.0, product_type="Term"
            ),
        )
    )
    acq, _ = encode_expense(portfolio, table, t_max=3)
    assert acq[0, 0] == 100.0
    assert acq[1, 0] == 0.0


def test_empty_table_is_all_zero():
    portfolio = Portfolio(policies=(_policy(),))
    acq, maint = encode_expense(portfolio, ExpenseTable(components=()), t_max=3)
    np.testing.assert_array_equal(acq, np.zeros((1, 3)))
    np.testing.assert_array_equal(maint, np.zeros((1, 3)))
