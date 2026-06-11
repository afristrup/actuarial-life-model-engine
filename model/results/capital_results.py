"""
Structured capital result contracts.

Purpose:
- provide stable SCR output interfaces
- separate capital calculations from reporting
- support downstream aggregation workflows

Key principle:
Result objects are pure data containers.

Architecture flow:
Base valuation
+
Stressed valuation
→ SCRResult
"""

class SCRResult:
    """
    Structured output of a univariate SCR calculation.

    Pure data container:
    - no capital calculation logic
    - no scenario logic
    - no aggregation logic
    """

    def __init__(
        self,
        scenario_id: str,
        risk_type: str,
        aggregation_category,
        base_bel: float,
        stressed_bel: float
    ):

        self.scenario_id = scenario_id
        self.risk_type = risk_type
        self.aggregation_category = aggregation_category
        self.base_bel = base_bel
        self.stressed_bel = stressed_bel

    @property
    def scr(self):

        return abs(
            self.stressed_bel
            - self.base_bel
        )

    def to_dict(self):

        return {
            "scenario_id": self.scenario_id,
            "risk_type": self.risk_type,
            "aggregation_category": self.aggregation_category,
            "base_bel": float(self.base_bel),
            "stressed_bel": float(self.stressed_bel),
            "scr": float(self.scr)
        }

    def __repr__(self):

        return (
            f"SCRResult("
            f"scenario_id={self.scenario_id}, "
            f"risk_type={self.risk_type}, "
            f"aggregation_category="f"{self.aggregation_category}, "
            f"scr={self.scr:.2f}"
            f")"
        )