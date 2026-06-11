from __future__ import annotations

from typing import NamedTuple

import jax.numpy as jnp


class ProjectionArrays(NamedTuple):
    prob_inforce: jnp.ndarray         # (N, T)
    qx: jnp.ndarray                   # (N, T)
    lapse_rate: jnp.ndarray           # (N, T)
    expected_premium: jnp.ndarray     # (N, T)
    expected_claim: jnp.ndarray       # (N, T)
    expected_lapse: jnp.ndarray       # (N, T)
    expected_acquisition: jnp.ndarray # (N, T)
    expected_maintenance: jnp.ndarray # (N, T)
    expected_total_expense: jnp.ndarray  # (N, T)
