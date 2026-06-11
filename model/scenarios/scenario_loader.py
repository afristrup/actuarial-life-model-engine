"""
Scenario calibration ingestion framework.

Responsibilities:
- load scenario calibration
- validate scenario structure
- construct ScenarioDefinition objects

Design principle:
Scenario definitions are calibration containers.
"""

import pandas as pd

from model.scenarios.scenario_definition import (
    ScenarioDefinition
)

from model.scenarios.scenario_validation import (
    validate_required_columns,
    validate_scenario_consistency,
    validate_supported_stresses
)


def load_scenarios(path):
    """
    Load scenarios from CSV calibration.
    """

    df = pd.read_csv(path)

    validate_required_columns(df)

    validate_scenario_consistency(df)

    validate_supported_stresses(df)

    grouped = df.groupby(
        "scenario_id"
    )

    scenarios = []

    for (
        scenario_id,
        group
    ) in grouped:

        first_row = group.iloc[0]

        stresses = {
            row["stress_name"]:
                row["stress_value"]
            for _, row
            in group.iterrows()
        }

        scenario = ScenarioDefinition(
            scenario_id=scenario_id,

            risk_type=
                first_row["risk_type"],

            aggregation_category=
                first_row[
                    "aggregation_category"
                ],

            name=first_row["name"],

            enabled=bool(
                first_row["enabled"]
            ),

            stresses=stresses
        )

        scenarios.append(
            scenario
        )

    return scenarios