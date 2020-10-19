import os
from   pathlib     import Path
from   morecontext import dirrollback

def test_dirrollback_nop():
    starting_dir = os.getcwd()
    with dirrollback():
        assert os.getcwd() == starting_dir
    assert os.getcwd() == starting_dir

def test_dirrollback_inner_changed(tmp_path):
    starting_dir = os.getcwd()
    assert Path(starting_dir) != tmp_path
    with dirrollback():
        assert os.getcwd() == starting_dir
        os.chdir(tmp_path)
    assert os.getcwd() == starting_dir
