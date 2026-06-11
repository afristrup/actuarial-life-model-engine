from __future__ import annotations

import jax
import jax.numpy as jnp

from lifebook.engine.projection_arrays import ProjectionArrays
from lifebook.engine.valuation_arrays import ValuationArrays


@jax.jit
def value(projection: ProjectionArrays, discount: jnp.ndarray) -> ValuationArrays:
    d = discount[None, :]

    pv_premium = projection.expected_premium * d
    pv_claim = projection.expected_claim * d
    pv_acq = projection.expected_acquisition * d
    pv_maint = projection.expected_maintenance * d
    pv_total_expense = pv_acq + pv_maint
    pv_net = pv_premium - pv_claim - pv_total_expense

    net_cashflow = (
        projection.expected_premium
        - projection.expected_claim
        - projection.expected_total_expense
    )

    pv_premiums_per_policy = jnp.sum(pv_premium, axis=1)
    pv_claims_per_policy = jnp.sum(pv_claim, axis=1)
    pv_expenses_per_policy = jnp.sum(pv_total_expense, axis=1)
    net_value_per_policy = (
        pv_premiums_per_policy - pv_claims_per_policy - pv_expenses_per_policy
    )

    return ValuationArrays(
        pv_premium=pv_premium,
        pv_claim=pv_claim,
        pv_acquisition=pv_acq,
        pv_maintenance=pv_maint,
        pv_total_expense=pv_total_expense,
        pv_net=pv_net,
        net_cashflow=net_cashflow,
        pv_premiums_per_policy=pv_premiums_per_policy,
        pv_claims_per_policy=pv_claims_per_policy,
        pv_expenses_per_policy=pv_expenses_per_policy,
        net_value_per_policy=net_value_per_policy,
    )
