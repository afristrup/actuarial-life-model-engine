from __future__ import annotations

from functools import partial

import jax
import jax.numpy as jnp

from lifebook.engine.projection_arrays import ProjectionArrays


@partial(jax.jit, static_argnames=())
def project(
    qx: jnp.ndarray,            # (N, T)
    lapse: jnp.ndarray,         # (N, T)
    acquisition: jnp.ndarray,   # (N, T)
    maintenance: jnp.ndarray,   # (N, T)
    premium: jnp.ndarray,       # (N,)
    sum_assured: jnp.ndarray,   # (N,)
    term: jnp.ndarray,          # (N,) int
) -> ProjectionArrays:
    n, t_max = qx.shape
    t_index = jnp.arange(t_max)
    mask = (t_index[None, :] < term[:, None]).astype(qx.dtype)

    survival = 1.0 - qx - lapse
    shifted = jnp.concatenate(
        [jnp.ones((n, 1), dtype=qx.dtype), survival[:, :-1]], axis=1
    )
    prob_inforce = jnp.cumprod(shifted, axis=1)

    expected_premium = premium[:, None] * prob_inforce * mask
    expected_claim = sum_assured[:, None] * prob_inforce * qx * mask
    expected_acq = acquisition * prob_inforce * mask
    expected_maint = maintenance * prob_inforce * mask
    expected_total = expected_acq + expected_maint
    expected_lapse = prob_inforce * lapse * mask

    return ProjectionArrays(
        prob_inforce=prob_inforce * mask,
        qx=qx * mask,
        lapse_rate=lapse * mask,
        expected_premium=expected_premium,
        expected_claim=expected_claim,
        expected_lapse=expected_lapse,
        expected_acquisition=expected_acq,
        expected_maintenance=expected_maint,
        expected_total_expense=expected_total,
    )
