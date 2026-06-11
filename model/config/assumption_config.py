class AssumptionConfig:
    """
    Centralised assumption ingestion configuration.

    Responsibilities:
    - own assumption file paths
    - centralise workflow assumption inputs
    - support scalable assumption expansion

    Does NOT:
    - load assumptions
    - perform validation
    - construct providers
    """

    def __init__(
        self,
        mortality_table_path,
        mortality_parameter_path=None,
        yield_curve_path=None,
        lapse_table_path=None,
        expense_table_path=None
    ):

        self.mortality_table_path = (
            mortality_table_path
        )

        self.mortality_parameter_path = (
            mortality_parameter_path
        )

        self.yield_curve_path = (
            yield_curve_path
        )

        self.lapse_table_path = (
            lapse_table_path
        )

        self.expense_table_path = (
            expense_table_path
        )

    def __repr__(self):

        return (
            f"AssumptionConfig("
            f"mortality_table_path="
            f"{self.mortality_table_path}, "
            f"yield_curve_path="
            f"{self.yield_curve_path}"
            f")"
        )