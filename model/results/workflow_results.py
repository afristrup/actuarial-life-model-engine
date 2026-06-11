from typing import Dict, List, Optional


class CapitalWorkflowResult:
    """
    Structured output of the full capital workflow.

    Responsibilities:
    - hold workflow outputs
    - package orchestration results
    - provide stable reporting contracts

    Does NOT:
    - run projections
    - run valuations
    - calculate SCRs
    - perform aggregation
    """

    __slots__ = [
        "base_result",
        "scenario_results",
        "scr_results",
        "life_scr",
        "market_scr",
        "bscr"
    ]

    def __init__(
        self,
        base_result,
        scenario_results: Dict[str, object],
        scr_results: List[object],
        life_scr=None,
        market_scr=None,
        bscr=None
    ):

        self.base_result = base_result

        self.scenario_results = (
            scenario_results
        )

        self.scr_results = scr_results

        self.life_scr = life_scr

        self.market_scr = market_scr

        self.bscr = bscr

    @property
    def base_bel(self) -> float:
        """
        Base Best Estimate Liability.
        """

        return (
            self.base_result
            .best_estimate_liability
        )

    @property
    def total_scr(self) -> Optional[float]:
        """
        Diversified BSCR amount.
        """

        if self.bscr is None:
            return None

        return self.bscr.diversified_scr

    def __repr__(self):

        return (
            f"CapitalWorkflowResult("
            f"base_bel={self.base_bel:.2f}, "
            f"scr_count={len(self.scr_results)}, "
            f"life_scr={'Yes' if self.life_scr else 'No'}, "
            f"market_scr={'Yes' if self.market_scr else 'No'}, "
            f"bscr={'Yes' if self.bscr else 'No'}"
            f")"
        )