"""
Correlation matrix ingestion layer.

Responsibilities:
- load correlation matrices from CSV
- validate correlation structure
- construct CorrelationMatrix objects

Does NOT:
- perform aggregation
- perform capital calculations

Design principle:
Validation occurs only at ingestion boundaries.
"""

import pandas as pd
import numpy as np

from model.capital.correlation import (
    CorrelationMatrix
)

from model.capital.correlation_validation import (
    validate_square_matrix,
    validate_symmetric_matrix,
    validate_matching_dimensions,
    validate_unique_risk_types,
    validate_matching_headers
)


def load_correlation_matrix(path):
    """
    Load correlation matrix from CSV.

    Responsibilities:
    - read CSV
    - validate matrix structure
    - construct CorrelationMatrix

    Does NOT:
    - perform aggregation
    - perform capital calculations
    """

    df = pd.read_csv(
        path,
        index_col=0
    )

    risk_types = list(df.columns)

    row_labels = list(df.index)

    validate_matching_headers(
        row_labels,
        risk_types
    )

    validate_unique_risk_types(
        risk_types
    )

    matrix = df.to_numpy(dtype=float)

    validate_square_matrix(
        matrix
    )

    validate_symmetric_matrix(
        matrix
    )

    validate_matching_dimensions(
        matrix,
        risk_types
    )

    return CorrelationMatrix(
        matrix=matrix,
        risk_types=risk_types
    )