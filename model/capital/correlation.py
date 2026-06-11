"""
Correlation matrix provider infrastructure.

Responsibilities:
- store correlation matrices
- validate matrix structure
- provide correlation lookup
- support matrix subsetting

Does NOT:
- perform SCR aggregation
- run capital calculations
- load CSV files

Architecture:
CSV/Data
→ loader
→ validation
→ CorrelationMatrix
→ aggregation engine
"""

import numpy as np

from model.capital.correlation_validation import (
    validate_square_matrix,
    validate_symmetric_matrix,
    validate_matching_dimensions,
    validate_unique_risk_types
)


class CorrelationMatrix:
    """
    Structured provider for correlation matrices.

    Pure provider object:
    - no aggregation logic
    - no scenario logic
    """

    def __init__(
        self,
        matrix,
        risk_types
    ):

        validate_square_matrix(matrix)

        validate_symmetric_matrix(matrix)

        validate_matching_dimensions(
            matrix,
            risk_types
        )

        validate_unique_risk_types(
            risk_types
        )

        self.matrix = matrix

        self.risk_types = risk_types

        self.index_map = {
            risk: index
            for index, risk
            in enumerate(risk_types)
        }

    def get_correlation(
        self,
        risk_a,
        risk_b
    ):
        """
        Return correlation between two risks.
        """

        i = self.index_map[risk_a]

        j = self.index_map[risk_b]

        return self.matrix[i, j]

    def subset(
        self,
        risk_types
    ):
        """
        Return subset correlation matrix.

        Preserves original matrix ordering.
        """

        missing_risks = [
            risk
            for risk in risk_types
            if risk not in self.risk_types
        ]

        if missing_risks:

            raise ValueError(
                f"Unknown risks requested: "
                f"{missing_risks}"
            )
        
        ordered_risks = [
            risk
            for risk in self.risk_types
            if risk in risk_types
        ]

        indices = [
            self.index_map[risk]
            for risk in ordered_risks
        ]

        subset_matrix = self.matrix[
            np.ix_(indices, indices)
        ]

        return CorrelationMatrix(
            matrix=subset_matrix,
            risk_types=ordered_risks
        )

    def __repr__(self):

        return (
            f"CorrelationMatrix("
            f"risks={self.risk_types}"
            f")"
        )