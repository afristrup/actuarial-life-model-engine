from __future__ import annotations

import numpy as np

from lifebook.encode.encode_portfolio import encode_portfolio
from lifebook.models.policy import Policy
from lifebook.models.portfolio import Portfolio


def test_roundtrip():
    portfolio = Portfolio(
        policies=(
            Policy(
                age=40, term=20, sum_assured=100_000.0, premium=500.0,
                gender="M", smoker_status="Smoker", product_type="Term", weight=3,
            ),
            Policy(
                age=55, term=10, sum_assured=200_000.0, premium=1200.0,
                gender="F", smoker_status="Non-Smoker", product_type="Endowment", weight=1,
            ),
        )
    )
    out = encode_portfolio(portfolio)
    np.testing.assert_array_equal(out.age, [40, 55])
    np.testing.assert_array_equal(out.term, [20, 10])
    np.testing.assert_allclose(out.sum_assured, [100_000.0, 200_000.0])
    np.testing.assert_allclose(out.premium, [500.0, 1200.0])
    np.testing.assert_allclose(out.weight, [3.0, 1.0])
