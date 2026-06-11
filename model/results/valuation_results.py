"""
Structured valuation result contracts.

Purpose:
- provide stable valuation output interfaces
- separate valuation mechanics from analytics
- support downstream reporting and capital workflows

Key principle:
Result objects are pure data containers.

Architecture flow:
ProjectionResult
→ ValuationRow
→ ValuationResult
"""

from typing import List, Dict, Optional

class ValuationRow:
    """
    Represents valuation results for a single projection period.

    Pure data container:
    - no valuation logic
    - no analytics

    Used inside ValuationResult.breakdown
    """

    __slots__ = [
        "t",
        "age",
        "discount_factor",
        "lapse_rate",
        "expected_premium",
        "expected_claim",
        "expected_lapse",
        "net_cashflow",
        "pv_premium",
        "pv_claim",
        "pv_net",
        "pv_acquisition_expense",
        "pv_maintenance_expense",
        "pv_total_expense",
        "cum_profit",
        "cum_cashflow"
    ]

    def __init__(
        self,
        t: int,
        age: int,
        discount_factor: float,
        lapse_rate: float,
        expected_premium: float,
        expected_claim: float,
        expected_lapse: float,
        net_cashflow: float,
        pv_premium: float,
        pv_claim: float,
        pv_acquisition_expense: float,
        pv_maintenance_expense: float,
        pv_total_expense: float,
        pv_net: float,
        cum_profit: float = 0.0,
        cum_cashflow: float = 0.0
    ):

        self.t = t
        self.age = age
        self.discount_factor = discount_factor
        self.expected_premium = expected_premium
        self.expected_claim = expected_claim
        self.lapse_rate = lapse_rate
        self.expected_lapse = expected_lapse
        self.net_cashflow = net_cashflow
        self.pv_premium = pv_premium
        self.pv_claim = pv_claim
        self.pv_acquisition_expense = (
            pv_acquisition_expense
        )
        self.pv_maintenance_expense = (
            pv_maintenance_expense
        )
        self.pv_total_expense = (
            pv_total_expense
        )
        self.pv_net = pv_net
        self.cum_profit = cum_profit
        self.cum_cashflow = cum_cashflow

    def to_dict(self):

        return {
            "t": self.t,
            "age": self.age,
            "discount_factor": self.discount_factor,
            "lapse_rate": self.lapse_rate,
            "expected_premium": self.expected_premium,
            "expected_claim": self.expected_claim,
            "expected_lapse": self.expected_lapse,
            "net_cashflow": self.net_cashflow,
            "pv_premium": self.pv_premium,
            "pv_claim": self.pv_claim,
            "pv_acquisition_expense":
                self.pv_acquisition_expense,
            "pv_maintenance_expense":
                self.pv_maintenance_expense,
            "pv_total_expense":
                self.pv_total_expense,
            "pv_net": self.pv_net,
            "cum_profit": self.cum_profit,
            "cum_cashflow": self.cum_cashflow
        }

    def __repr__(self):

        return (
            f"ValuationRow("
            f"t={self.t}, "
            f"pv_net={self.pv_net:.2f}"
            f")"
        )

class ValuationResult:
    """
    Structured output of a policy valuation.

    Fields:
    - pv_premiums: Present value of premiums
    - pv_claims: Present value of claims
    - net_value: Net present value
    - breakdown: Optional per-period results

    Design:
    - Pure data container
    - No actuarial or analytical logic

    Acts as the contract between valuation and analysis layers

    """

    __slots__ = ["pv_premiums", "pv_claims", "pv_expenses", "net_value", "breakdown"]

    def __init__(
        self,
        pv_premiums: float,
        pv_claims: float,
        pv_expenses: float,
        net_value: float,
        breakdown: Optional[List[Dict]] = None
    ):
        # Basic validation (lightweight, no behaviour change)
        if breakdown is not None and not isinstance(breakdown, list):
            raise TypeError("breakdown must be a list of dictionaries or None")

        # Explicit typing (contract clarity)
        self.pv_premiums: float = pv_premiums
        self.pv_claims: float = pv_claims
        self.pv_expenses: float = pv_expenses
        self.net_value: float = net_value
        self.breakdown: Optional[List[Dict]] = breakdown

    @property
    def best_estimate_liability(self) -> float:
        """
        Solvency-style Best Estimate Liability (BEL).

        Positive BEL represents a liability.
        """

        return (
            self.pv_claims
            + self.pv_expenses
            - self.pv_premiums
        )

    @property
    def pv_future_profit(self) -> float:
        """
        Present Value of Future Profits (PVFP).

        Positive PVFP represents expected future profit.
        """

        return -self.best_estimate_liability
    
    # Provided for backward compatibility and easy serialisation
    def to_dict(self) -> dict:
        """
        Convert to dictionary (for backward compatibility).
        """
        result = {
            "pv_premiums": self.pv_premiums,
            "pv_claims": self.pv_claims,
            "pv_expenses": self.pv_expenses,
            "net_value": self.net_value,
            "best_estimate_liability": self.best_estimate_liability,
            "pv_future_profit": self.pv_future_profit
        }

        if self.breakdown is not None:
            result["breakdown"] = self.breakdown

        return result

    def __repr__(self):
        return (
            f"ValuationResult("
            f"pv_premiums={self.pv_premiums:.2f}, "
            f"pv_claims={self.pv_claims:.2f}, "
            f"pv_expenses={self.pv_expenses:.2f}, "
            f"BEL={self.best_estimate_liability:.2f}, "
            f"PVFP={self.pv_future_profit:.2f}, "
            f"breakdown={'Yes' if self.breakdown else 'No'}"
            f")"
        )