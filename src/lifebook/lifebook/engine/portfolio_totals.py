from __future__ import annotations

from typing import NamedTuple

import jax.numpy as jnp


class PortfolioTotals(NamedTuple):
    pv_premiums: jnp.ndarray  # scalar
    pv_claims: jnp.ndarray    # scalar
    pv_expenses: jnp.ndarray  # scalar
    net_value: jnp.ndarray    # scalar
