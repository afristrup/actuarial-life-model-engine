from __future__ import annotations

from pathlib import Path

import pytest

from lifebook.loaders.load_mortality_table import load_mortality_table


def _write(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "mort.csv"
    p.write_text(content)
    return p


def test_loads_keyed_by_gender_age(tmp_path: Path):
    table = load_mortality_table(
        _write(tmp_path, "gender,age,qx\nM,40,0.001\nF,40,0.0008\n")
    )
    assert table.rates[("M", 40)] == 0.001
    assert table.rates[("F", 40)] == 0.0008


def test_missing_column(tmp_path: Path):
    with pytest.raises(ValueError, match="missing columns"):
        load_mortality_table(_write(tmp_path, "age,qx\n40,0.001\n"))


def test_negative_age(tmp_path: Path):
    with pytest.raises(ValueError, match="negative age"):
        load_mortality_table(_write(tmp_path, "gender,age,qx\nM,-1,0.001\n"))


def test_qx_out_of_range(tmp_path: Path):
    with pytest.raises(ValueError, match="out of"):
        load_mortality_table(_write(tmp_path, "gender,age,qx\nM,40,1.5\n"))


def test_duplicate_gender_age(tmp_path: Path):
    with pytest.raises(ValueError, match="duplicate"):
        load_mortality_table(
            _write(tmp_path, "gender,age,qx\nM,40,0.001\nM,40,0.002\n")
        )
