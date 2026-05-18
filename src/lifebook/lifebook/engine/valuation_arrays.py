from __future__ import annotations

from typing import NamedTuple

import jax.numpy as jnp


class ValuationArrays(NamedTuple):
    # per-(policy, t) discounted cashflows
    pv_premium: jnp.ndarray                # (N, T)
    pv_claim: jnp.ndarray                  # (N, T)
    pv_acquisition: jnp.ndarray            # (N, T)
    pv_maintenance: jnp.ndarray            # (N, T)
    pv_total_expense: jnp.ndarray          # (N, T)
    pv_net: jnp.ndarray                    # (N, T)
    net_cashflow: jnp.ndarray              # (N, T) undiscounted net
    # per-policy aggregates
    pv_premiums_per_policy: jnp.ndarray    # (N,)
    pv_claims_per_policy: jnp.ndarray      # (N,)
    pv_expenses_per_policy: jnp.ndarray    # (N,)
    net_value_per_policy: jnp.ndarray      # (N,)
