"""
Structured projection result contracts.

Purpose:
- provide stable projection output interfaces
- separate projection mechanics from downstream layers
- support valuation and analytical workflows

Key principle:
Result objects are pure data containers.

Architecture flow:
Projection
→ ProjectionRow
→ ProjectionResult
"""

from typing import List, Dict, Optional

class ProjectionRow:
    """
    Represents one projected time period.

    Pure data container:
    - no projection logic
    - no actuarial calculations

    Used as the structured output of projection.py
    """

    __slots__ = [
        "t",
        "age",
        "prob_inforce",
        "qx",
        "lapse_rate",
        "expected_premium",
        "expected_claim",
        "expected_lapse",
        "expected_acquisition_expense",
        "expected_maintenance_expense",
        "expected_total_expense",
    ]

    def __init__(
        self,
        t: int,
        age: int,
        prob_inforce: float,
        qx: float,
        lapse_rate: float,
        expected_premium: float,
        expected_claim: float,
        expected_lapse: float,
        expected_acquisition_expense: float,
        expected_maintenance_expense: float,
        expected_total_expense: float
    ):

        self.t = t
        self.age = age
        self.prob_inforce = prob_inforce
        self.qx = qx
        self.lapse_rate = lapse_rate
        self.expected_premium = expected_premium
        self.expected_claim = expected_claim
        self.expected_lapse = expected_lapse
        self.expected_acquisition_expense = (
    expected_acquisition_expense
)
        self.expected_maintenance_expense = (
    expected_maintenance_expense
)
        self.expected_total_expense = (
    expected_total_expense
)

    def to_dict(self) -> dict:
        """
        Convert to dictionary for compatibility/debugging.
        """

        return {
            "t": self.t,
            "age": self.age,
            "prob_inforce": self.prob_inforce,
            "qx": self.qx,
            "lapse_rate": self.lapse_rate,
            "expected_premium": self.expected_premium,
            "expected_claim": self.expected_claim,
            "expected_lapse": self.expected_lapse,
            "expected_acquisition_expense":
                self.expected_acquisition_expense,
            "expected_maintenance_expense":
                self.expected_maintenance_expense,
            "expected_total_expense":
                self.expected_total_expense,
        }

    def __repr__(self):

        return (
            f"ProjectionRow("
            f"t={self.t}, "
            f"age={self.age}, "
            f"prob_inforce={self.prob_inforce:.6f}, "
            f"qx={self.qx:.6f}"
            f")"
        )

class ProjectionResult:
    """
    Container for projected policy cashflows.

    Holds all projection rows produced during projection.

    Design:
    - structured output contract
    - no actuarial logic
    """

    __slots__ = ["rows"]

    def __init__(self, rows: List[ProjectionRow]):

        if not isinstance(rows, list):
            raise TypeError("rows must be a list")

        self.rows = rows

    def to_dict(self) -> dict:
        """
        Convert projection rows into serialisable format.
        """

        return {
            "rows": [row.to_dict() for row in self.rows]
        }

    def __repr__(self):

        return (
            f"ProjectionResult("
            f"rows={len(self.rows)}"
            f")"
        )