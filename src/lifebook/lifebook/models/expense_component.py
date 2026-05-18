from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ExpenseComponent(BaseModel):
    model_config = ConfigDict(frozen=True)

    expense_type: Literal["acquisition", "maintenance"]
    amount_type: Literal["fixed", "premium_pct"]
    value: float = Field(ge=0.0)
    product_type: str | None = None
