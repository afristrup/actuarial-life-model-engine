class ScenarioConfig:
    """
    Centralised scenario execution configuration.

    Responsibilities:
    - own scenario calibration inputs
    - centralise scenario execution configuration
    - support future scenario extensibility

    Does NOT:
    - load scenarios
    - apply stresses
    - perform calculations
    """

    def __init__(
        self,
        scenario_path,
        enabled_categories=None
    ):

        self.scenario_path = (
            scenario_path
        )

        self.enabled_categories = (
            enabled_categories
        )

    def __repr__(self):

        return (
            f"ScenarioConfig("
            f"scenario_path="
            f"{self.scenario_path}"
            f")"
        )