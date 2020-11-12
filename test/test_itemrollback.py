import pytest
from   morecontext import itemrollback

def test_itemrollback_nop():
    d = {"foo": 42}
    with itemrollback(d, 'foo'):
        assert d["foo"] == 42
    assert d["foo"] == 42

def test_itemrollback_nop_error():
    d = {"foo": 42}
    with pytest.raises(RuntimeError, match='Catch this!'):
        with itemrollback(d, 'foo'):
            assert d["foo"] == 42
            raise RuntimeError('Catch this!')
    assert d["foo"] == 42

def test_itemrollback_modify():
    d = {"foo": 42}
    with itemrollback(d, 'foo'):
        assert d["foo"] == 42
        d["foo"] = [3.14]
    assert d["foo"] == 42

def test_itemrollback_modify_error():
    d = {"foo": 42}
    with pytest.raises(RuntimeError, match='Catch this!'):
        with itemrollback(d, 'foo'):
            assert d["foo"] == 42
            d["foo"] = [3.14]
            raise RuntimeError('Catch this!')
    assert d["foo"] == 42

def test_itemrollback_del():
    d = {"foo": 42}
    with itemrollback(d, 'foo'):
        assert d["foo"] == 42
        del d["foo"]
    assert d["foo"] == 42

def test_itemrollback_del_error():
    d = {"foo": 42}
    with pytest.raises(RuntimeError, match='Catch this!'):
        with itemrollback(d, 'foo'):
            assert d["foo"] == 42
            del d["foo"]
            raise RuntimeError('Catch this!')
    assert d["foo"] == 42

def test_itemrollback_unset():
    d = {"foo": 42}
    with itemrollback(d, 'bar'):
        assert "bar" not in d
    assert "bar" not in d

def test_itemrollback_unset_error():
    d = {"foo": 42}
    with pytest.raises(RuntimeError, match='Catch this!'):
        with itemrollback(d, 'bar'):
            assert "bar" not in d
            raise RuntimeError('Catch this!')
    assert "bar" not in d

def test_itemrollback_unset_modify():
    d = {"foo": 42}
    with itemrollback(d, 'bar'):
        assert "bar" not in d
        d["bar"] = [3.14]
    assert "bar" not in d

def test_itemrollback_unset_modify_error():
    d = {"foo": 42}
    with pytest.raises(RuntimeError, match='Catch this!'):
        with itemrollback(d, 'bar'):
            assert "bar" not in d
            d["bar"] = [3.14]
            raise RuntimeError('Catch this!')
    assert "bar" not in d

def test_itemrollback_no_copy():
    d = {"foo": {"bar": [1, 2, 3], "quux": ["a", "b", "c"]}}
    with itemrollback(d, "foo"):
        d["foo"]["bar"].append(4)
        d["foo"]["quux"] = ["x", "y", "z"]
    assert d["foo"] == {"bar": [1, 2, 3, 4], "quux": ["x", "y", "z"]}

def test_itemrollback_no_copy_error():
    d = {"foo": {"bar": [1, 2, 3], "quux": ["a", "b", "c"]}}
    with pytest.raises(RuntimeError, match='Catch this!'):
        with itemrollback(d, "foo"):
            d["foo"]["bar"].append(4)
            d["foo"]["quux"] = ["x", "y", "z"]
            raise RuntimeError('Catch this!')
    assert d["foo"] == {"bar": [1, 2, 3, 4], "quux": ["x", "y", "z"]}

def test_itemrollback_copy():
    d = {"foo": {"bar": [1, 2, 3], "quux": ["a", "b", "c"]}}
    with itemrollback(d, "foo", copy=True):
        d["foo"]["bar"].append(4)
        d["foo"]["quux"] = ["x", "y", "z"]
    assert d["foo"] == {"bar": [1, 2, 3, 4], "quux": ["a", "b", "c"]}

def test_itemrollback_copy_error():
    d = {"foo": {"bar": [1, 2, 3], "quux": ["a", "b", "c"]}}
    with pytest.raises(RuntimeError, match='Catch this!'):
        with itemrollback(d, "foo", copy=True):
            d["foo"]["bar"].append(4)
            d["foo"]["quux"] = ["x", "y", "z"]
            raise RuntimeError('Catch this!')
    assert d["foo"] == {"bar": [1, 2, 3, 4], "quux": ["a", "b", "c"]}

@pytest.mark.parametrize('copy', [False, True])
def test_itemrollback_deepcopy(copy):
    d = {"foo": {"bar": [1, 2, 3], "quux": ["a", "b", "c"]}}
    with itemrollback(d, "foo", copy=copy, deepcopy=True):
        d["foo"]["bar"].append(4)
        d["foo"]["quux"] = ["x", "y", "z"]
    assert d["foo"] == {"bar": [1, 2, 3], "quux": ["a", "b", "c"]}

@pytest.mark.parametrize('copy', [False, True])
def test_itemrollback_deepcopy_error(copy):
    d = {"foo": {"bar": [1, 2, 3], "quux": ["a", "b", "c"]}}
    with pytest.raises(RuntimeError, match='Catch this!'):
        with itemrollback(d, "foo", copy=copy, deepcopy=True):
            d["foo"]["bar"].append(4)
            d["foo"]["quux"] = ["x", "y", "z"]
            raise RuntimeError('Catch this!')
    assert d["foo"] == {"bar": [1, 2, 3], "quux": ["a", "b", "c"]}
