from __future__ import annotations

from pathlib import Path

import pytest

from lifebook.loaders.load_smoker_multipliers import load_smoker_multipliers


def _write(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "smoker.csv"
    p.write_text(content)
    return p


def test_loads(tmp_path: Path):
    mults = load_smoker_multipliers(
        _write(tmp_path, "smoker_status,mortality_multiplier\nSmoker,1.75\nNon-Smoker,1.0\n")
    )
    assert mults.multipliers == {"Smoker": 1.75, "Non-Smoker": 1.0}


def test_missing_column(tmp_path: Path):
    with pytest.raises(ValueError, match="missing columns"):
        load_smoker_multipliers(_write(tmp_path, "smoker_status\nSmoker\n"))


def test_negative_multiplier(tmp_path: Path):
    with pytest.raises(ValueError, match="negative"):
        load_smoker_multipliers(
            _write(tmp_path, "smoker_status,mortality_multiplier\nSmoker,-1\n")
        )


def test_duplicate(tmp_path: Path):
    with pytest.raises(ValueError, match="duplicate"):
        load_smoker_multipliers(
            _write(
                tmp_path,
                "smoker_status,mortality_multiplier\nSmoker,1.5\nSmoker,2.0\n",
            )
        )
