from __future__ import annotations

import jax.numpy as jnp
import numpy as np

import lifebook  # noqa: F401
from lifebook.engine.project import project
from lifebook.engine.value import value


def test_pv_applies_discount_per_t():
    qx = jnp.array([[0.0, 0.0]])  # no decrement → prob_inforce = 1 throughout
    lapse = jnp.zeros((1, 2))
    zeros = jnp.zeros((1, 2))
    projection = project(
        qx, lapse, zeros, zeros,
        premium=jnp.array([100.0]),
        sum_assured=jnp.array([0.0]),
        term=jnp.array([2]),
    )
    discount = jnp.array([1.0, 1 / 1.05])
    out = value(projection, discount)
    np.testing.assert_allclose(np.asarray(out.pv_premium[0]), [100.0, 100.0 / 1.05])


def test_per_policy_totals_sum_pv():
    qx = jnp.array([[0.0, 0.0, 0.0]])
    lapse = jnp.zeros((1, 3))
    zeros = jnp.zeros((1, 3))
    projection = project(
        qx, lapse, zeros, zeros,
        premium=jnp.array([100.0]),
        sum_assured=jnp.array([0.0]),
        term=jnp.array([3]),
    )
    discount = jnp.array([1.0, 1.0, 1.0])
    out = value(projection, discount)
    assert float(out.pv_premiums_per_policy[0]) == 300.0
    assert float(out.net_value_per_policy[0]) == 300.0  # no claims, no expenses
