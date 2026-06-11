# jaxtabular

Polars feature engineering into JAX training loops. Three pure functions, one per file.

```python
from jaxtabular import engineer, batches, train
import jax.numpy as jnp, polars as pl

df = pl.read_parquet("data.parquet")
X, y = engineer(df, [pl.col("x") * 10], target="t")

def step(params, Xb, yb):
    pred = Xb @ params
    loss = jnp.mean((pred - yb) ** 2)
    grad = 2 * Xb.T @ (pred - yb) / Xb.shape[0]
    return params - 0.01 * grad, loss

params, history = train(
    step=step,
    params=jnp.zeros(X.shape[1]),
    epoch_batches=lambda e: batches(X, y, size=128, seed=e),
    epochs=10,
)
```

## Design

- **One signature per file.** `engineer.py`, `batches.py`, `train.py`.
- **No hidden state.** Pure functions; outputs of one feed the next.
- **Fail fast.** Shape mismatches, missing targets, oversized batches raise at the call boundary, not three steps later.
- **Static shapes.** `batches` drops the partial tail so JAX `jit` compiles once.
- **No PyTorch DataLoader.** Tabular data fits in memory after `engineer`; slicing two NumPy arrays beats `list(zip(...))` collation.
