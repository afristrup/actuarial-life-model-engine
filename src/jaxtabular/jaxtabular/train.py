from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

import jax


def train(
    step: Callable[[Any, Any, Any], tuple[Any, Any]],
    params: Any,
    epoch_batches: Callable[[int], Iterable[tuple[Any, Any]]],
    epochs: int,
) -> tuple[Any, list[float]]:
    if epochs <= 0:
        raise ValueError(f"epochs must be positive, got {epochs}")

    jitted = jax.jit(step)
    history: list[float] = []

    for epoch in range(epochs):
        total = 0.0
        count = 0
        for X_batch, y_batch in epoch_batches(epoch):
            params, loss = jitted(params, X_batch, y_batch)
            total += float(loss)
            count += 1
        if count == 0:
            raise ValueError(f"epoch {epoch} produced zero batches")
        history.append(total / count)

    return params, history
