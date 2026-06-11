from __future__ import annotations

from typing import NamedTuple

from lifebook.encode.encode_portfolio import PortfolioArrays
from lifebook.engine.portfolio_totals import PortfolioTotals
from lifebook.engine.projection_arrays import ProjectionArrays
from lifebook.engine.valuation_arrays import ValuationArrays


class PortfolioResult(NamedTuple):
    totals: PortfolioTotals
    valuation: ValuationArrays
    projection: ProjectionArrays
    arrays: PortfolioArrays
    policy_ids: tuple[str | None, ...]
    policy_count: int
