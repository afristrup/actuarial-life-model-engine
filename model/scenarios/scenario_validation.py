from model.scenarios.stress_registry import (
    SUPPORTED_STRESSES
)

REQUIRED_COLUMNS = [
    "scenario_id",
    "risk_type",
    "aggregation_category",
    "name",
    "enabled",
    "stress_name",
    "stress_value"
]


def validate_required_columns(df):
    """
    Validate required scenario columns exist.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing required columns: "
            f"{missing_columns}"
        )


def validate_scenario_consistency(df):
    """
    Validate scenario metadata consistency.

    Ensures:
    - same scenario_id always maps to
      same metadata fields
    """

    grouped = df.groupby(
        "scenario_id"
    )

    metadata_fields = [
        "risk_type",
        "aggregation_category",
        "name",
        "enabled"
    ]

    for (
        scenario_id,
        group
    ) in grouped:

        for field in metadata_fields:

            unique_values = (
                group[field]
                .unique()
                .tolist()
            )

            if len(unique_values) > 1:

                raise ValueError(
                    f"Inconsistent "
                    f"{field} values for "
                    f"scenario_id="
                    f"{scenario_id}"
                )
            
def validate_supported_stresses(df):
    """
    Validate all stresses are supported.
    """

    configured_stresses = set(
        df["stress_name"]
    )

    unsupported_stresses = (
        configured_stresses
        - SUPPORTED_STRESSES
    )

    if unsupported_stresses:

        raise ValueError(
            f"Unsupported stresses found: "
            f"{sorted(unsupported_stresses)}"
        )            