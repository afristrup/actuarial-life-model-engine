from __future__ import annotations

from pathlib import Path

import pytest

from lifebook.loaders.load_expense_table import load_expense_table


def _write(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "expense.csv"
    p.write_text(content)
    return p


def test_loads(tmp_path: Path):
    table = load_expense_table(
        _write(
            tmp_path,
            "expense_type,amount_type,value\nacquisition,fixed,40\nmaintenance,premium_pct,0.02\n",
        )
    )
    assert len(table.components) == 2
    assert table.components[0].expense_type == "acquisition"


def test_missing_column(tmp_path: Path):
    with pytest.raises(ValueError, match="missing columns"):
        load_expense_table(_write(tmp_path, "expense_type,value\nacquisition,40\n"))


def test_bad_expense_type(tmp_path: Path):
    with pytest.raises(ValueError, match="expense_type"):
        load_expense_table(
            _write(tmp_path, "expense_type,amount_type,value\nmystery,fixed,40\n")
        )


def test_bad_amount_type(tmp_path: Path):
    with pytest.raises(ValueError, match="amount_type"):
        load_expense_table(
            _write(tmp_path, "expense_type,amount_type,value\nacquisition,wibble,40\n")
        )


def test_negative_value(tmp_path: Path):
    with pytest.raises(ValueError, match="negative"):
        load_expense_table(
            _write(tmp_path, "expense_type,amount_type,value\nacquisition,fixed,-10\n")
        )
