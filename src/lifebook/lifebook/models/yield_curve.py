from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class YieldCurve(BaseModel):
    model_config = ConfigDict(frozen=True)

    spot_rates: dict[float, float] = Field(min_length=1)
