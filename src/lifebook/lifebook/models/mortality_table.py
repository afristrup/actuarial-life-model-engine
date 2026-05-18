from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MortalityTable(BaseModel):
    model_config = ConfigDict(frozen=True)

    rates: dict[tuple[str, int], float] = Field(min_length=1)
