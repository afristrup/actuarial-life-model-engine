# lifebook

JAX-vectorised life insurance valuation engine. Pydantic at the input boundary, dense float64 arrays inside, `jit` + scan over time, `vmap` across policies.

## Layout

- `models/` — pydantic value objects (`Policy`, `Portfolio`, `MortalityTable`, `LapseTable`, `ExpenseTable`, `YieldCurve`, `SmokerMultipliers`, `Assumptions`).
- `loaders/` — CSV → pydantic.
- `encode/` — pydantic → dense JAX-ready arrays.
- `engine/` — pure JAX: `project`, `value`, `aggregate`.
- `analysis/` — pull breakdowns into polars DataFrames.
- `run.py` — `value_portfolio(portfolio, assumptions, *, return_breakdown=False)`.

## Design

One signature per file. Pydantic validates once at the entry boundary; the engine never sees raw user input. Per-policy term differences are handled by padding to `T_max` and masking. Fidelity check in `tests/test_parity.py` proves identical PVs to the legacy `model/` engine on `data/portfolios/sample_portfolio.csv` at `rtol=1e-9`.

## Status

- Engine: complete, parity-tested at `rtol=1e-9` on the 250-policy sample portfolio.
- Legacy `model/` directory remains in place as the parity oracle — do not delete until notebooks migrate.
- Notebooks (`notebooks/*.ipynb`) still import `model.*`; rewriting them onto `lifebook.value_portfolio` is a separate task.

## Running

```bash
cd src/lifebook
uv sync --group dev
uv run pytest tests/       # 5 parity tests
uv run pyrefly check       # 0 errors
```
