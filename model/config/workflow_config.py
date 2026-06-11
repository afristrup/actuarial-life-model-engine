class CapitalWorkflowConfig:
    """
    Unified capital workflow execution configuration.

    Responsibilities:
    - centralise workflow execution inputs
    - compose workflow configuration objects
    - support future frontend integration

    Does NOT:
    - execute workflow logic
    - load files
    - perform calculations
    """

    def __init__(
        self,
        portfolio_path,
        assumption_config,
        scenario_config,
        correlation_config,
        return_breakdown=False
    ):

        self.portfolio_path = (
            portfolio_path
        )

        self.scenario_config = (
            scenario_config
        )

        self.assumption_config = (
            assumption_config
        )

        self.correlation_config = (
            correlation_config
        )

        self.return_breakdown = (
            return_breakdown
        )

    def __repr__(self):

        return (
            f"CapitalWorkflowConfig("
            f"portfolio_path="
            f"{self.portfolio_path}, "
            f"scenario_config="
            f"{self.scenario_config}"
            f")"
        )