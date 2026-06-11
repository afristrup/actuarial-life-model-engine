from __future__ import annotations

from pathlib import Path
from typing import Any

from lifebook.loaders.load_expense_table import load_expense_table
from lifebook.loaders.load_lapse_table import load_lapse_table
from lifebook.loaders.load_mortality_table import load_mortality_table
from lifebook.loaders.load_smoker_multipliers import load_smoker_multipliers
from lifebook.loaders.load_yield_curve import load_yield_curve
from lifebook.models.assumptions import Assumptions


def load_assumptions(
    *,
    mortality_path: str | Path,
    yield_curve_path: str | Path,
    smoker_multipliers_path: str | Path | None = None,
    lapse_path: str | Path | None = None,
    expense_path: str | Path | None = None,
) -> Assumptions:
    kwargs: dict[str, Any] = {
        "mortality": load_mortality_table(mortality_path),
        "yield_curve": load_yield_curve(yield_curve_path),
    }
    if smoker_multipliers_path is not None:
        kwargs["smoker_multipliers"] = load_smoker_multipliers(smoker_multipliers_path)
    if lapse_path is not None:
        kwargs["lapse"] = load_lapse_table(lapse_path)
    if expense_path is not None:
        kwargs["expenses"] = load_expense_table(expense_path)
    return Assumptions(**kwargs)
