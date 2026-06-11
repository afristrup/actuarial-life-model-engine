from __future__ import annotations

from collections.abc import Iterator

import numpy as np


def batches(
    X: np.ndarray,
    y: np.ndarray,
    size: int,
    *,
    shuffle: bool = True,
    seed: int = 0,
) -> Iterator[tuple[np.ndarray, np.ndarray]]:
    if X.shape[0] != y.shape[0]:
        raise ValueError(f"row count mismatch: X={X.shape[0]} y={y.shape[0]}")
    if size <= 0:
        raise ValueError(f"size must be positive, got {size}")
    if X.shape[0] < size:
        raise ValueError(f"need at least one full batch: rows={X.shape[0]} < size={size}")

    n = X.shape[0]
    idx = np.arange(n)
    if shuffle:
        np.random.default_rng(seed).shuffle(idx)

    n_full = (n // size) * size
    for start in range(0, n_full, size):
        sl = idx[start : start + size]
        yield X[sl], y[sl]
