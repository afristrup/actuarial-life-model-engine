"""
SCR aggregation framework.

Responsibilities:
- aggregate SCR results
- apply correlation diversification
- construct aligned SCR vectors
- produce structured aggregation outputs

Does NOT:
- run scenarios
- perform valuation logic
- apply stresses
"""

import numpy as np

from model.results import (
    AggregatedSCRResult
)


def aggregate_scrs(
    scr_results,
    correlation_matrix,
    risk_category
):
    """
    Aggregate SCRs using correlation matrices.
    """

    if not scr_results:

        raise ValueError(
            "scr_results cannot be empty."
        )

    component_scrs = {
        scr.risk_type: scr
        for scr in scr_results
    }

    available_risks = list(
        component_scrs.keys()
    )

    subset_matrix = (
        correlation_matrix.subset(
            available_risks
        )
    )

    ordered_scrs = [
        component_scrs[risk]
        for risk
        in subset_matrix.risk_types
    ]

    scr_vector = np.array([
        scr.scr
        for scr in ordered_scrs
    ])

    diversified_scr = np.sqrt(
        scr_vector.T
        @ subset_matrix.matrix
        @ scr_vector
    )

    gross_scr = np.sum(scr_vector)

    return AggregatedSCRResult(
        risk_category=risk_category,
        gross_scr=gross_scr,
        diversified_scr=diversified_scr,
        component_scrs=component_scrs,
        correlation_matrix=subset_matrix
    )

def aggregate_life_scr(
    scr_results,
    correlation_matrix
):
    """
    Aggregate life SCRs.
    """

    return aggregate_scrs(
        scr_results=scr_results,
        correlation_matrix=correlation_matrix,
        risk_category="life"
    )

def aggregate_market_scr(
    scr_results,
    correlation_matrix
):
    """
    Aggregate market SCRs.
    """

    return aggregate_scrs(
        scr_results=scr_results,
        correlation_matrix=correlation_matrix,
        risk_category="market"
    )

def aggregate_basic_scr(
    life_scr,
    market_scr,
    correlation_matrix
):
    """
    Aggregate BSCR components.
    """

    from model.results import (
        SCRResult
    )

    life_component = SCRResult(
        scenario_id="life_aggregated",
        risk_type="life",
        aggregation_category="bscr",
        base_bel=0.0,
        stressed_bel=life_scr.diversified_scr
    )

    market_component = SCRResult(
        scenario_id="market_aggregated",
        risk_type="market",
        aggregation_category="bscr",
        base_bel=0.0,
        stressed_bel=market_scr.diversified_scr
    )

    return aggregate_scrs(
        scr_results=[
            life_component,
            market_component
        ],
        correlation_matrix=correlation_matrix,
        risk_category="bscr"
    )