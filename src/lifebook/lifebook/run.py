from __future__ import annotations

import jax.numpy as jnp

from lifebook.encode.encode_discount import encode_discount
from lifebook.encode.encode_expense import encode_expense
from lifebook.encode.encode_lapse import encode_lapse
from lifebook.encode.encode_portfolio import encode_portfolio
from lifebook.encode.encode_qx import encode_qx
from lifebook.engine.aggregate import aggregate
from lifebook.engine.project import project
from lifebook.engine.value import value
from lifebook.models.assumptions import Assumptions
from lifebook.models.portfolio import Portfolio
from lifebook.portfolio_result import PortfolioResult


def value_portfolio(portfolio: Portfolio, assumptions: Assumptions) -> PortfolioResult:
    arrays = encode_portfolio(portfolio)
    t_max = int(arrays.term.max())

    qx = encode_qx(portfolio, assumptions.mortality, assumptions.smoker_multipliers, t_max)
    lapse = encode_lapse(portfolio, assumptions.lapse, t_max)
    acquisition, maintenance = encode_expense(portfolio, assumptions.expenses, t_max)
    discount = encode_discount(assumptions.yield_curve, t_max)

    projection = project(
        jnp.asarray(qx),
        jnp.asarray(lapse),
        jnp.asarray(acquisition),
        jnp.asarray(maintenance),
        jnp.asarray(arrays.premium),
        jnp.asarray(arrays.sum_assured),
        jnp.asarray(arrays.term),
    )
    valuation = value(projection, jnp.asarray(discount))
    totals = aggregate(valuation, jnp.asarray(arrays.weight))

    return PortfolioResult(
        totals=totals,
        valuation=valuation,
        projection=projection,
        arrays=arrays,
        policy_ids=tuple(p.policy_id for p in portfolio.policies),
        policy_count=len(portfolio.policies),
    )
