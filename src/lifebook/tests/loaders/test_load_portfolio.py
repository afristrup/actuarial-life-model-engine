from __future__ import annotations

from pathlib import Path

import pytest

from lifebook.loaders.load_portfolio import load_portfolio

HEADER = "policy_id,age,term,sum_assured,premium,weight,gender,smoker_status,product_type\n"


def _write(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "portfolio.csv"
    p.write_text(content)
    return p


def test_loads_with_policy_id(tmp_path: Path):
    portfolio = load_portfolio(
        _write(
            tmp_path,
            HEADER + "POL1,40,20,100000,500,1,M,Smoker,Term\n",
        )
    )
    assert portfolio.policies[0].policy_id == "POL1"
    assert portfolio.policies[0].age == 40


def test_extra_columns_ignored(tmp_path: Path):
    portfolio = load_portfolio(
        _write(
            tmp_path,
            "age,term,sum_assured,premium,weight,gender,smoker_status,product_type,issue_year,region\n"
            "40,20,100000,500,1,M,Smoker,Term,2020,South\n",
        )
    )
    assert portfolio.policies[0].age == 40


def test_missing_column(tmp_path: Path):
    with pytest.raises(ValueError, match="missing columns"):
        load_portfolio(
            _write(tmp_path, "age,term,sum_assured\n40,20,100000\n")
        )


def test_invalid_term(tmp_path: Path):
    with pytest.raises(Exception):
        load_portfolio(
            _write(
                tmp_path,
                HEADER + "POL1,40,0,100000,500,1,M,Smoker,Term\n",
            )
        )
