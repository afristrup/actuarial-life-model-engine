from __future__ import annotations

import numpy as np

from lifebook.encode.encode_lapse import encode_lapse
from lifebook.models.lapse_segment import LapseSegment
from lifebook.models.lapse_table import LapseTable
from lifebook.models.policy import Policy
from lifebook.models.portfolio import Portfolio


def _policy(**overrides) -> Policy:
    base = dict(
        age=40, term=5, sum_assured=100_000.0, premium=500.0,
        gender="M", smoker_status="Smoker", product_type="Term", weight=1,
    )
    base.update(overrides)
    return Policy(**base)


def test_matching_segment_produces_rate():
    portfolio = Portfolio(policies=(_policy(),))
    table = LapseTable(
        segments=(
            LapseSegment(
                product_type="Term", smoker_status="Smoker",
                duration_start=1, duration_end=99, lapse_rate=0.1,
            ),
        )
    )
    out = encode_lapse(portfolio, table, t_max=3)
    # t=0 → duration=1, matches → 0.1
    np.testing.assert_allclose(out, [[0.1, 0.1, 0.1]])


def test_non_matching_product_returns_zero():
    portfolio = Portfolio(policies=(_policy(product_type="Endowment"),))
    table = LapseTable(
        segments=(
            LapseSegment(
                product_type="Term", smoker_status="Smoker",
                duration_start=1, duration_end=99, lapse_rate=0.1,
            ),
        )
    )
    out = encode_lapse(portfolio, table, t_max=3)
    np.testing.assert_array_equal(out, [[0.0, 0.0, 0.0]])


def test_duration_mapping_t_plus_one():
    portfolio = Portfolio(policies=(_policy(term=4),))
    # Segment covers durations 2-3 only — so t=1 and t=2 should match, t=0 and t=3 should not
    table = LapseTable(
        segments=(
            LapseSegment(
                product_type="Term", smoker_status="Smoker",
                duration_start=2, duration_end=3, lapse_rate=0.05,
            ),
        )
    )
    out = encode_lapse(portfolio, table, t_max=4)
    np.testing.assert_allclose(out, [[0.0, 0.05, 0.05, 0.0]])


def test_past_term_is_zero():
    portfolio = Portfolio(policies=(_policy(term=2),))
    table = LapseTable(
        segments=(
            LapseSegment(
                product_type="Term", smoker_status="Smoker",
                duration_start=1, duration_end=99, lapse_rate=0.1,
            ),
        )
    )
    out = encode_lapse(portfolio, table, t_max=4)
    assert out[0, 2] == 0.0 and out[0, 3] == 0.0


def test_empty_table_is_all_zero():
    portfolio = Portfolio(policies=(_policy(),))
    out = encode_lapse(portfolio, LapseTable(segments=()), t_max=3)
    np.testing.assert_array_equal(out, np.zeros((1, 3)))
