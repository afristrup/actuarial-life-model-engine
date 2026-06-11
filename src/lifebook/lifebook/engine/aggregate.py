from __future__ import annotations

import jax
import jax.numpy as jnp

from lifebook.engine.portfolio_totals import PortfolioTotals
from lifebook.engine.valuation_arrays import ValuationArrays


@jax.jit
def aggregate(valuation: ValuationArrays, weight: jnp.ndarray) -> PortfolioTotals:
    pv_premiums = jnp.sum(valuation.pv_premiums_per_policy * weight)
    pv_claims = jnp.sum(valuation.pv_claims_per_policy * weight)
    pv_expenses = jnp.sum(valuation.pv_expenses_per_policy * weight)
    net_value = pv_premiums - pv_claims - pv_expenses
    return PortfolioTotals(
        pv_premiums=pv_premiums,
        pv_claims=pv_claims,
        pv_expenses=pv_expenses,
        net_value=net_value,
    )
