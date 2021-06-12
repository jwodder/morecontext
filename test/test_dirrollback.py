import os
from pathlib import Path
import pytest
from morecontext import dirrollback


def test_dirrollback_nop() -> None:
    starting_dir = os.getcwd()
    with dirrollback():
        assert os.getcwd() == starting_dir
    assert os.getcwd() == starting_dir


def test_dirrollback_nop_error() -> None:
    starting_dir = os.getcwd()
    with pytest.raises(RuntimeError, match="Catch this!"):
        with dirrollback():
            assert os.getcwd() == starting_dir
            raise RuntimeError("Catch this!")
    assert os.getcwd() == starting_dir


def test_dirrollback_inner_changed(tmp_path: Path) -> None:
    starting_dir = os.getcwd()
    assert Path(starting_dir) != tmp_path
    with dirrollback():
        assert os.getcwd() == starting_dir
        os.chdir(tmp_path)
    assert os.getcwd() == starting_dir


def test_dirrollback_inner_changed_error(tmp_path: Path) -> None:
    starting_dir = os.getcwd()
    assert Path(starting_dir) != tmp_path
    with pytest.raises(RuntimeError, match="Catch this!"):
        with dirrollback():
            assert os.getcwd() == starting_dir
            os.chdir(tmp_path)
            raise RuntimeError("Catch this!")
    assert os.getcwd() == starting_dir
