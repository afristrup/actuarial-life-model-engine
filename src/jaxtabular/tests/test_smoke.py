from __future__ import annotations

import jax.numpy as jnp
import numpy as np
import polars as pl
import pytest

from jaxtabular import batches, engineer, train


def test_engineer_extracts_X_y():
    df = pl.DataFrame({"a": [1.0, 2.0, 3.0, 4.0], "b": [10.0, 20.0, 30.0, 40.0], "t": [0.0, 1.0, 0.0, 1.0]})
    X, y = engineer(df, [pl.col("a") * 2], target="t")
    assert X.shape == (4, 2)
    assert y.shape == (4,)
    np.testing.assert_array_equal(y, [0.0, 1.0, 0.0, 1.0])


def test_engineer_missing_target_fails_fast():
    df = pl.DataFrame({"a": [1.0]})
    with pytest.raises(ValueError, match="not in columns"):
        engineer(df, [], target="missing")


def test_engineer_all_nulls_fails_fast():
    df = pl.DataFrame({"a": [1.0, 2.0], "t": [None, None]}, schema={"a": pl.Float64, "t": pl.Float64})
    with pytest.raises(ValueError, match="no rows remain"):
        engineer(df, [], target="t")


def test_batches_static_shape_and_count():
    X = np.arange(20, dtype=np.float32).reshape(10, 2)
    y = np.arange(10, dtype=np.float32)
    out = list(batches(X, y, size=4, shuffle=False))
    assert len(out) == 2
    for xb, yb in out:
        assert xb.shape == (4, 2)
        assert yb.shape == (4,)


def test_batches_size_too_large_fails_fast():
    X = np.zeros((3, 2))
    y = np.zeros(3)
    with pytest.raises(ValueError, match="at least one full batch"):
        next(batches(X, y, size=4))


def test_batches_row_mismatch_fails_fast():
    with pytest.raises(ValueError, match="row count mismatch"):
        next(batches(np.zeros((4, 2)), np.zeros(3), size=2))


def test_end_to_end_linear_regression_converges():
    rng = np.random.default_rng(0)
    n, d = 256, 3
    true_w = np.array([1.5, -2.0, 0.5], dtype=np.float32)
    X_raw = rng.standard_normal((n, d)).astype(np.float32)
    y_raw = X_raw @ true_w
    df = pl.from_numpy(np.column_stack([X_raw, y_raw]), schema=["f0", "f1", "f2", "t"])

    X, y = engineer(df, [], target="t")

    def step(params, Xb, yb):
        pred = Xb @ params
        loss = jnp.mean((pred - yb) ** 2)
        grad = 2 * Xb.T @ (pred - yb) / Xb.shape[0]
        return params - 0.05 * grad, loss

    params, history = train(
        step=step,
        params=jnp.zeros(d, dtype=jnp.float32),
        epoch_batches=lambda e: batches(X, y, size=32, seed=e),
        epochs=20,
    )

    assert history[-1] < history[0]
    assert history[-1] < 0.05
    np.testing.assert_allclose(np.asarray(params), true_w, atol=0.1)


def test_train_zero_epochs_fails_fast():
    with pytest.raises(ValueError, match="epochs must be positive"):
        train(lambda p, x, y: (p, 0.0), params=0, epoch_batches=lambda e: [], epochs=0)
