from __future__ import annotations

from pathlib import Path

import pytest

from lifebook.loaders.load_yield_curve import load_yield_curve


def _write(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "yc.csv"
    p.write_text(content)
    return p


def test_loads_and_divides_by_100(tmp_path: Path):
    curve = load_yield_curve(_write(tmp_path, "t,spot_rate\n1,4.0\n2,4.5\n"))
    assert curve.spot_rates == {1.0: 0.04, 2.0: 0.045}


def test_missing_column(tmp_path: Path):
    with pytest.raises(ValueError, match="missing columns"):
        load_yield_curve(_write(tmp_path, "t\n1\n"))


def test_negative_maturity(tmp_path: Path):
    with pytest.raises(ValueError, match="negative maturity"):
        load_yield_curve(_write(tmp_path, "t,spot_rate\n-1,4.0\n"))


def test_duplicate_maturity(tmp_path: Path):
    with pytest.raises(ValueError, match="duplicate maturities"):
        load_yield_curve(_write(tmp_path, "t,spot_rate\n1,4.0\n1,5.0\n"))


def test_spot_rate_out_of_range(tmp_path: Path):
    with pytest.raises(ValueError, match="out of"):
        load_yield_curve(_write(tmp_path, "t,spot_rate\n1,150.0\n"))


def test_null_value(tmp_path: Path):
    with pytest.raises(ValueError, match="null"):
        load_yield_curve(_write(tmp_path, "t,spot_rate\n1,\n"))
