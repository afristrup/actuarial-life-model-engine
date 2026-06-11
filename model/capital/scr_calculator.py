"""
SCR calculation framework.

Responsibilities:
- calculate univariate SCR values
- consume valuation outputs
- preserve separation between
  scenarios and capital calculations

Does NOT:
- run projection logic
- run valuation logic
- apply scenario overlays
- perform aggregation
"""

from model.results import SCRResult

def calculate_scr(
    base_result,
    stressed_result,
    scenario
):
    """
    Calculate SCR from base and stressed BEL.
    """

    return SCRResult(
        scenario_id=scenario.scenario_id,
        risk_type=scenario.risk_type,
        aggregation_category=scenario.aggregation_category,

        base_bel=(
            base_result.best_estimate_liability
        ),

        stressed_bel=(
            stressed_result.best_estimate_liability
        )
    )