"""
Structured portfolio aggregation result contracts.

Purpose:
- provide stable portfolio-level output interfaces
- separate aggregation mechanics from analytics
- support downstream portfolio and capital analysis

Key principle:
Result objects are pure data containers.

Architecture flow:
ValuationResult
→ Portfolio aggregation
→ PortfolioResult
"""

from typing import List, Dict, Optional

class PortfolioResult:
    """
    Structured output of portfolio valuation.

    Aggregates results across multiple policies.

    Pure data container:
    - no valuation logic
    - no analytics
    """

    __slots__ = [
        "pv_premiums",
        "pv_claims",
        "pv_expenses",
        "net_value",
        "policy_count",
        "breakdown"
    ]

    def __init__(
        self,
        pv_premiums: float,
        pv_claims: float,
        pv_expenses: float,
        net_value: float,
        policy_count: int,
        breakdown=None
    ):

        self.pv_premiums = pv_premiums
        self.pv_claims = pv_claims
        self.pv_expenses = pv_expenses
        self.net_value = net_value
        self.policy_count = policy_count
        self.breakdown = breakdown

    @property
    def best_estimate_liability(self) -> float:

        return (
            self.pv_claims
            + self.pv_expenses
            - self.pv_premiums
        )

    @property
    def pv_future_profit(self) -> float:

        return -self.best_estimate_liability
    
    def to_dict(self):

        result = {
            "pv_premiums": self.pv_premiums,
            "pv_claims": self.pv_claims,
            "pv_expenses": self.pv_expenses,
            "best_estimate_liability": self.best_estimate_liability,
            "pv_future_profit": self.pv_future_profit,
            "net_value": self.net_value,
            "policy_count": self.policy_count
        }

        if self.breakdown is not None:
            result["breakdown"] = [
                row.to_dict() for row in self.breakdown
            ]

        return result

    def __repr__(self):

        return (
            f"PortfolioResult("
            f"policies={self.policy_count}, "
            f"pv_expenses={self.pv_expenses:.2f}, "
            f"BEL={self.best_estimate_liability:.2f}, "
            f"PVFP={self.pv_future_profit:.2f}"
            f")"
        )