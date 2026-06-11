from model.capital.scr_calculator import (
    calculate_scr
)

from .aggregation import (
    aggregate_scrs,
    aggregate_life_scr,
    aggregate_market_scr,
    aggregate_basic_scr
)

from .capital_workflow import (
    run_capital_framework
)

from .capital_workflow import (
    run_capital_framework,
    run_capital_workflow,
    load_workflow_assumptions,
    load_workflow_correlations,
    load_workflow_portfolio
)