from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from lifebook.models.lapse_segment import LapseSegment


class LapseTable(BaseModel):
    model_config = ConfigDict(frozen=True)

    segments: tuple[LapseSegment, ...] = ()
