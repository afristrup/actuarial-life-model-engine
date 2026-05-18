from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Policy(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    age: int = Field(ge=0, le=120)
    term: int = Field(ge=1, le=120)
    sum_assured: float = Field(gt=0)
    premium: float = Field(ge=0)
    gender: str = Field(min_length=1)
    smoker_status: str = Field(min_length=1)
    product_type: str = Field(min_length=1)
    weight: int = Field(ge=1, default=1)
    policy_id: str | None = None
