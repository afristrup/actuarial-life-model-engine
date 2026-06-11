class ScenarioDefinition:
    """
    Structured scenario definition.

    Represents:
    - scenario metadata
    - generic stress calibration payload

    Does NOT:
    - apply stresses
    - run projections
    - perform valuation logic
    """

    def __init__(
        self,
        scenario_id: str,
        risk_type: str,
        aggregation_category: str,
        name: str,
        stresses: dict,
        enabled: bool = True
    ):

        self.scenario_id = scenario_id

        self.risk_type = risk_type

        self.aggregation_category = (
            aggregation_category
        )

        self.name = name

        self.stresses = stresses

        self.enabled = enabled

    def get_stress(
        self,
        stress_name,
        default=None
    ):
        """
        Resolve stress parameter.
        """

        return self.stresses.get(
            stress_name,
            default
        )

    def __repr__(self):

        return (
            f"ScenarioDefinition("
            f"scenario_id="
            f"{self.scenario_id}, "
            f"risk_type="
            f"{self.risk_type}, "
            f"aggregation_category="
            f"{self.aggregation_category}"
            f")"
        )