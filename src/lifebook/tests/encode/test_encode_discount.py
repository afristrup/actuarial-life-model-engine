from __future__ import annotations

import numpy as np
import pytest

from lifebook.encode.encode_discount import encode_discount
from lifebook.models.yield_curve import YieldCurve


def test_t0_is_one():
    curve = YieldCurve(spot_rates={1.0: 0.05, 2.0: 0.05})
    df = encode_discount(curve, t_max=3)
    assert df[0] == 1.0


def test_known_curve():
    curve = YieldCurve(spot_rates={1.0: 0.05, 2.0: 0.05, 3.0: 0.05})
    df = encode_discount(curve, t_max=4)
    np.testing.assert_allclose(df, [1.0, 1 / 1.05, 1 / 1.05**2, 1 / 1.05**3])


def test_terminal_extrapolation():
    curve = YieldCurve(spot_rates={1.0: 0.04, 2.0: 0.05})
    df = encode_discount(curve, t_max=5)
    # t=3, t=4 use rate at max_term=2 → 0.05
    np.testing.assert_allclose(df[3], 1 / 1.05**3)
    np.testing.assert_allclose(df[4], 1 / 1.05**4)


def test_missing_integer_maturity_fails_fast():
    curve = YieldCurve(spot_rates={1.0: 0.04, 3.0: 0.05})  # no t=2
    with pytest.raises(ValueError, match="no spot rate"):
        encode_discount(curve, t_max=4)
