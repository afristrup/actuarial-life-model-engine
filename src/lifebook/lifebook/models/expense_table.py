from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from lifebook.models.expense_component import ExpenseComponent


class ExpenseTable(BaseModel):
    model_config = ConfigDict(frozen=True)

    components: tuple[ExpenseComponent, ...] = ()
