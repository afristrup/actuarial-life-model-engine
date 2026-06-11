import numpy as np


def validate_square_matrix(matrix):
    """
    Validate that the matrix is square.
    """

    rows, cols = matrix.shape

    if rows != cols:

        raise ValueError(
            "Correlation matrix must be square."
        )


def validate_symmetric_matrix(matrix):
    """
    Validate that the matrix is symmetric.
    """

    if not np.allclose(matrix, matrix.T):

        raise ValueError(
            "Correlation matrix must be symmetric."
        )


def validate_matching_dimensions(
    matrix,
    risk_types
):
    """
    Validate that matrix dimensions match
    the number of risk types.
    """

    if matrix.shape[0] != len(risk_types):

        raise ValueError(
            "Matrix dimensions do not match "
            "number of risk types."
        )


def validate_unique_risk_types(risk_types):
    """
    Validate that risk types are unique.
    """

    if len(risk_types) != len(set(risk_types)):

        raise ValueError(
            "Duplicate risk types found."
        )
    
def validate_matching_headers(
    row_labels,
    column_labels
):
    """
    Validate that row and column labels match.
    """

    if row_labels != column_labels:

        raise ValueError(
            "Row and column labels do not match."
        )