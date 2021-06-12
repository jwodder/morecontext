import os
from pathlib import Path
import pytest
from morecontext import dirchanged


def test_dirchanged(tmp_path: Path) -> None:
    starting_dir = os.getcwd()
    assert Path(starting_dir) != tmp_path
    with dirchanged(tmp_path):
        assert Path(os.getcwd()) == tmp_path
    assert os.getcwd() == starting_dir


def test_dirchanged_str(tmp_path: Path) -> None:
    starting_dir = os.getcwd()
    assert Path(starting_dir) != tmp_path
    with dirchanged(str(tmp_path)):
        assert Path(os.getcwd()) == tmp_path
    assert os.getcwd() == starting_dir


def test_dirchanged_error(tmp_path: Path) -> None:
    starting_dir = os.getcwd()
    assert Path(starting_dir) != tmp_path
    with pytest.raises(RuntimeError, match="Catch this!"):
        with dirchanged(tmp_path):
            assert Path(os.getcwd()) == tmp_path
            raise RuntimeError("Catch this!")
    assert os.getcwd() == starting_dir


def test_dirchanged_inner_changed(tmp_path: Path) -> None:
    starting_dir = os.getcwd()
    assert Path(starting_dir) != tmp_path
    with dirchanged(tmp_path):
        assert Path(os.getcwd()) == tmp_path
        (tmp_path / "foo").mkdir()
        os.chdir(tmp_path / "foo")
    assert os.getcwd() == starting_dir


def test_dirchanged_inner_changed_error(tmp_path: Path) -> None:
    starting_dir = os.getcwd()
    assert Path(starting_dir) != tmp_path
    with pytest.raises(RuntimeError, match="Catch this!"):
        with dirchanged(tmp_path):
            assert Path(os.getcwd()) == tmp_path
            (tmp_path / "foo").mkdir()
            os.chdir(tmp_path / "foo")
            raise RuntimeError("Catch this!")
    assert os.getcwd() == starting_dir
