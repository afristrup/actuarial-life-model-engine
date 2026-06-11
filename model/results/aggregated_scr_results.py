"""
Structured diversified SCR result contracts.

Purpose:
- provide stable aggregation output interfaces
- separate aggregation logic from reporting
- support downstream capital workflows

Key principle:
Result objects are pure data containers.

Architecture flow:
SCRResult[]
+
CorrelationMatrix
→ aggregation
→ AggregatedSCRResult
"""


class AggregatedSCRResult:
    """
    Structured output of SCR aggregation.

    Pure data container:
    - no aggregation logic
    - no scenario logic
    - no valuation logic
    """

    def __init__(
        self,
        risk_category: str,
        gross_scr,
        diversified_scr,
        component_scrs,
        correlation_matrix
    ):

        self.risk_category = risk_category

        self.gross_scr = gross_scr

        self.diversified_scr = diversified_scr

        self.component_scrs = component_scrs

        self.correlation_matrix = (
            correlation_matrix
        )

    @property
    def diversification_benefit(self):
        """
        Diversification reduction produced
        by correlation aggregation.
        """

        return (
            self.gross_scr
            - self.diversified_scr
        )

    def to_dict(self):

        return {
            "risk_category":
                self.risk_category,

            "gross_scr":
                float(self.gross_scr),

            "diversified_scr":
                float(self.diversified_scr),

            "diversification_benefit":
                float(self.diversification_benefit),

            "component_scrs": {
                risk: scr.to_dict()
                for risk, scr
                in self.component_scrs.items()
            },

            "correlation_risks":
                self.correlation_matrix.risk_types
        }

    def __repr__(self):

        return (
            f"AggregatedSCRResult("
            f"risk_category="
            f"{self.risk_category}, "
            f"gross_scr="
            f"{self.gross_scr:.2f}, "
            f"diversified_scr="
            f"{self.diversified_scr:.2f}"
            f")"
        )