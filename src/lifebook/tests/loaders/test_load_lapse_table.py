from __future__ import annotations

from pathlib import Path

import pytest

from lifebook.loaders.load_lapse_table import load_lapse_table

HEADER = "product_type,smoker_status,duration_start,duration_end,lapse_rate\n"


def _write(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "lapse.csv"
    p.write_text(content)
    return p


def test_loads(tmp_path: Path):
    table = load_lapse_table(
        _write(tmp_path, HEADER + "Term,Smoker,0,5,0.1\nTerm,Smoker,6,99,0.05\n")
    )
    assert len(table.segments) == 2
    assert table.segments[0].lapse_rate == 0.1


def test_missing_column(tmp_path: Path):
    with pytest.raises(ValueError, match="missing columns"):
        load_lapse_table(_write(tmp_path, "product_type,lapse_rate\nTerm,0.1\n"))


def test_duration_end_before_start(tmp_path: Path):
    with pytest.raises(ValueError, match="duration_end"):
        load_lapse_table(_write(tmp_path, HEADER + "Term,Smoker,5,1,0.1\n"))


def test_duplicate_segment(tmp_path: Path):
    with pytest.raises(ValueError, match="duplicate"):
        load_lapse_table(
            _write(tmp_path, HEADER + "Term,Smoker,0,5,0.1\nTerm,Smoker,0,5,0.2\n")
        )


def test_overlapping_ranges(tmp_path: Path):
    with pytest.raises(ValueError, match="overlapping"):
        load_lapse_table(
            _write(tmp_path, HEADER + "Term,Smoker,0,5,0.1\nTerm,Smoker,3,10,0.05\n")
        )


def test_rate_out_of_range(tmp_path: Path):
    with pytest.raises(ValueError):
        load_lapse_table(_write(tmp_path, HEADER + "Term,Smoker,0,5,1.5\n"))
