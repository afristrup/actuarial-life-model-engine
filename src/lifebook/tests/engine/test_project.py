from __future__ import annotations

import jax.numpy as jnp
import numpy as np

import lifebook  # noqa: F401 — enables x64
from lifebook.engine.project import project


def test_prob_inforce_evolves_by_decrement():
    # Single policy, 3 years, qx=0.01 constant, lapse=0.05 constant
    qx = jnp.array([[0.01, 0.01, 0.01]])
    lapse = jnp.array([[0.05, 0.05, 0.05]])
    zeros = jnp.zeros((1, 3))
    out = project(
        qx, lapse, zeros, zeros,
        premium=jnp.array([100.0]),
        sum_assured=jnp.array([1000.0]),
        term=jnp.array([3]),
    )
    survival = 1.0 - 0.01 - 0.05
    np.testing.assert_allclose(
        np.asarray(out.prob_inforce[0]),
        [1.0, survival, survival**2],
        rtol=1e-12,
    )


def test_expected_premium_and_claim():
    qx = jnp.array([[0.1, 0.1]])
    lapse = jnp.zeros((1, 2))
    zeros = jnp.zeros((1, 2))
    out = project(
        qx, lapse, zeros, zeros,
        premium=jnp.array([100.0]),
        sum_assured=jnp.array([1000.0]),
        term=jnp.array([2]),
    )
    # t=0: prob_inforce=1, premium=100, claim=1000 * 0.1 = 100
    # t=1: prob_inforce=0.9, premium=90, claim=1000 * 0.9 * 0.1 = 90
    np.testing.assert_allclose(np.asarray(out.expected_premium[0]), [100.0, 90.0])
    np.testing.assert_allclose(np.asarray(out.expected_claim[0]), [100.0, 90.0])


def test_term_mask_zeros_past_term():
    qx = jnp.array([[0.01, 0.01, 0.01, 0.01]])
    lapse = jnp.zeros((1, 4))
    zeros = jnp.zeros((1, 4))
    out = project(
        qx, lapse, zeros, zeros,
        premium=jnp.array([100.0]),
        sum_assured=jnp.array([1000.0]),
        term=jnp.array([2]),
    )
    # Past t=1 (term=2 means t=0,1 active) everything must be zero
    np.testing.assert_array_equal(np.asarray(out.expected_premium[0, 2:]), [0.0, 0.0])
    np.testing.assert_array_equal(np.asarray(out.expected_claim[0, 2:]), [0.0, 0.0])


def test_per_policy_different_terms():
    qx = jnp.array([[0.01, 0.01, 0.01], [0.02, 0.02, 0.02]])
    lapse = jnp.zeros((2, 3))
    zeros = jnp.zeros((2, 3))
    out = project(
        qx, lapse, zeros, zeros,
        premium=jnp.array([100.0, 200.0]),
        sum_assured=jnp.array([1000.0, 2000.0]),
        term=jnp.array([2, 3]),
    )
    # Policy 0 (term=2) zero at t=2; policy 1 (term=3) nonzero throughout
    assert float(out.expected_premium[0, 2]) == 0.0
    assert float(out.expected_premium[1, 2]) > 0.0
