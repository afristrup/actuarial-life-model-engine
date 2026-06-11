class CorrelationConfig:
    """
    Centralised correlation matrix configuration.

    Responsibilities:
    - own correlation matrix file paths
    - centralise aggregation dependencies

    Does NOT:
    - load matrices
    - perform aggregation
    """

    def __init__(
        self,
        life_correlation_path,
        market_correlation_path,
        bscr_correlation_path
    ):

        self.life_correlation_path = (
            life_correlation_path
        )

        self.market_correlation_path = (
            market_correlation_path
        )

        self.bscr_correlation_path = (
            bscr_correlation_path
        )

    def __repr__(self):

        return (
            f"CorrelationConfig("
            f"life={self.life_correlation_path}, "
            f"market={self.market_correlation_path}, "
            f"bscr={self.bscr_correlation_path}"
            f")"
        )