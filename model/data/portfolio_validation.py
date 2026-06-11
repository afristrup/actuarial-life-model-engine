REQUIRED_COLUMNS = [
    "age",
    "term",
    "sum_assured",
    "premium"
]


def validate_required_columns(df):
    """
    Validate that all required modelling columns exist.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )