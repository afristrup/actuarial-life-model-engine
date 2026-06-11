from __future__ import annotations

import jax.numpy as jnp

import lifebook  # noqa: F401
from lifebook.engine.aggregate import aggregate
from lifebook.engine.valuation_arrays import ValuationArrays


def _empty_2d(n: int) -> jnp.ndarray:
    return jnp.zeros((n, 1))


def test_weighted_sum():
    n = 3
    v = ValuationArrays(
        pv_premium=_empty_2d(n),
        pv_claim=_empty_2d(n),
        pv_acquisition=_empty_2d(n),
        pv_maintenance=_empty_2d(n),
        pv_total_expense=_empty_2d(n),
        pv_net=_empty_2d(n),
        net_cashflow=_empty_2d(n),
        pv_premiums_per_policy=jnp.array([100.0, 200.0, 300.0]),
        pv_claims_per_policy=jnp.array([10.0, 20.0, 30.0]),
        pv_expenses_per_policy=jnp.array([1.0, 2.0, 3.0]),
        net_value_per_policy=jnp.array([89.0, 178.0, 267.0]),
    )
    weight = jnp.array([1.0, 2.0, 3.0])
    totals = aggregate(v, weight)
    # premiums: 100*1 + 200*2 + 300*3 = 1400
    assert float(totals.pv_premiums) == 1400.0
    # claims: 10 + 40 + 90 = 140
    assert float(totals.pv_claims) == 140.0
    # expenses: 1 + 4 + 9 = 14
    assert float(totals.pv_expenses) == 14.0
    # net: 1400 - 140 - 14 = 1246
    assert float(totals.net_value) == 1246.0
