import os
from   pathlib     import Path
from   morecontext import dirchanged

def test_dirchanged(tmp_path):
    starting_dir = os.getcwd()
    assert Path(starting_dir) != tmp_path
    with dirchanged(tmp_path):
        assert Path(os.getcwd()) == tmp_path
    assert os.getcwd() == starting_dir

def test_dirchanged_inner_changed(tmp_path):
    starting_dir = os.getcwd()
    assert Path(starting_dir) != tmp_path
    with dirchanged(tmp_path):
        assert Path(os.getcwd()) == tmp_path
        (tmp_path / "foo").mkdir()
        os.chdir(tmp_path / "foo")
    assert os.getcwd() == starting_dir
