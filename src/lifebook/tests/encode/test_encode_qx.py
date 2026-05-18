from __future__ import annotations

import numpy as np
import pytest

from lifebook.encode.encode_qx import encode_qx
from lifebook.models.mortality_table import MortalityTable
from lifebook.models.policy import Policy
from lifebook.models.portfolio import Portfolio
from lifebook.models.smoker_multipliers import SmokerMultipliers


def _portfolio(**overrides) -> Portfolio:
    base = dict(
        age=40, term=3, sum_assured=100_000.0, premium=500.0,
        gender="M", smoker_status="Smoker", product_type="Term", weight=1,
    )
    base.update(overrides)
    return Portfolio(policies=(Policy(**base),))


def test_basic_lookup_no_smoker_multipliers():
    portfolio = _portfolio()
    mortality = MortalityTable(rates={
        ("M", 40): 0.01, ("M", 41): 0.011, ("M", 42): 0.012,
    })
    qx = encode_qx(portfolio, mortality, None, t_max=3)
    np.testing.assert_allclose(qx, [[0.01, 0.011, 0.012]])


def test_smoker_multiplier_applied():
    portfolio = _portfolio()
    mortality = MortalityTable(rates={("M", a): 0.01 for a in (40, 41, 42)})
    smoker = SmokerMultipliers(multipliers={"Smoker": 2.0, "Non-Smoker": 1.0})
    qx = encode_qx(portfolio, mortality, smoker, t_max=3)
    np.testing.assert_allclose(qx, [[0.02, 0.02, 0.02]])


def test_qx_clamped_to_one():
    portfolio = _portfolio()
    mortality = MortalityTable(rates={("M", a): 0.6 for a in (40, 41, 42)})
    smoker = SmokerMultipliers(multipliers={"Smoker": 3.0})
    qx = encode_qx(portfolio, mortality, smoker, t_max=3)
    np.testing.assert_array_equal(qx, [[1.0, 1.0, 1.0]])


def test_past_term_is_zero():
    portfolio = _portfolio(term=2)
    mortality = MortalityTable(rates={("M", a): 0.01 for a in (40, 41, 42)})
    qx = encode_qx(portfolio, mortality, None, t_max=3)
    assert qx[0, 2] == 0.0
    np.testing.assert_allclose(qx[0, :2], [0.01, 0.01])


def test_unknown_gender_fails_fast():
    portfolio = _portfolio(gender="X")
    mortality = MortalityTable(rates={("M", 40): 0.01})
    with pytest.raises(ValueError, match="no mortality rates for genders"):
        encode_qx(portfolio, mortality, None, t_max=1)


def test_attained_age_out_of_range_fails_fast():
    portfolio = _portfolio(age=40, term=5)
    mortality = MortalityTable(rates={("M", a): 0.01 for a in (40, 41, 42)})
    with pytest.raises(ValueError, match="exceeds mortality table"):
        encode_qx(portfolio, mortality, None, t_max=5)


def test_unknown_smoker_status_fails_fast():
    portfolio = _portfolio(smoker_status="Mystery")
    mortality = MortalityTable(rates={("M", a): 0.01 for a in (40, 41, 42)})
    smoker = SmokerMultipliers(multipliers={"Smoker": 1.0})
    with pytest.raises(ValueError, match="no smoker multiplier"):
        encode_qx(portfolio, mortality, smoker, t_max=3)
