from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from lifebook.models.policy import Policy


class Portfolio(BaseModel):
    model_config = ConfigDict(frozen=True)

    policies: tuple[Policy, ...] = Field(min_length=1)
