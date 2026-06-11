from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SmokerMultipliers(BaseModel):
    model_config = ConfigDict(frozen=True)

    multipliers: dict[str, float] = Field(min_length=1)
