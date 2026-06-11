from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator


class LapseSegment(BaseModel):
    model_config = ConfigDict(frozen=True)

    product_type: str = Field(min_length=1)
    smoker_status: str = Field(min_length=1)
    duration_start: int = Field(ge=0)
    duration_end: int = Field(ge=0)
    lapse_rate: float = Field(ge=0.0, le=1.0)

    @model_validator(mode="after")
    def _check_range(self) -> "LapseSegment":
        if self.duration_end < self.duration_start:
            raise ValueError(
                f"duration_end={self.duration_end} < duration_start={self.duration_start}"
            )
        return self
