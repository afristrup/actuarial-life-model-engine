from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from lifebook.models.expense_table import ExpenseTable
from lifebook.models.lapse_table import LapseTable
from lifebook.models.mortality_table import MortalityTable
from lifebook.models.smoker_multipliers import SmokerMultipliers
from lifebook.models.yield_curve import YieldCurve


class Assumptions(BaseModel):
    model_config = ConfigDict(frozen=True)

    mortality: MortalityTable
    yield_curve: YieldCurve
    smoker_multipliers: SmokerMultipliers | None = None
    lapse: LapseTable = LapseTable()
    expenses: ExpenseTable = ExpenseTable()
