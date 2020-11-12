from   types       import SimpleNamespace
import pytest
from   morecontext import attrrollback

def test_attrrollback_nop():
    obj = SimpleNamespace(foo=42)
    with attrrollback(obj, 'foo'):
        assert obj.foo == 42
    assert obj.foo == 42

def test_attrrollback_nop_error():
    obj = SimpleNamespace(foo=42)
    with pytest.raises(RuntimeError, match='Catch this!'):
        with attrrollback(obj, 'foo'):
            assert obj.foo == 42
            raise RuntimeError('Catch this!')
    assert obj.foo == 42

def test_attrrollback_modify():
    obj = SimpleNamespace(foo=42)
    with attrrollback(obj, 'foo'):
        assert obj.foo == 42
        obj.foo = [3.14]
    assert obj.foo == 42

def test_attrrollback_modify_error():
    obj = SimpleNamespace(foo=42)
    with pytest.raises(RuntimeError, match='Catch this!'):
        with attrrollback(obj, 'foo'):
            assert obj.foo == 42
            obj.foo = [3.14]
            raise RuntimeError('Catch this!')
    assert obj.foo == 42

def test_attrrollback_del():
    obj = SimpleNamespace(foo=42)
    with attrrollback(obj, 'foo'):
        assert obj.foo == 42
        del obj.foo
    assert obj.foo == 42

def test_attrrollback_del_error():
    obj = SimpleNamespace(foo=42)
    with pytest.raises(RuntimeError, match='Catch this!'):
        with attrrollback(obj, 'foo'):
            assert obj.foo == 42
            del obj.foo
            raise RuntimeError('Catch this!')
    assert obj.foo == 42

def test_attrrollback_unset():
    obj = SimpleNamespace(foo=42)
    with attrrollback(obj, 'bar'):
        assert not hasattr(obj, "bar")
    assert not hasattr(obj, "bar")

def test_attrrollback_unset_error():
    obj = SimpleNamespace(foo=42)
    with pytest.raises(RuntimeError, match='Catch this!'):
        with attrrollback(obj, 'bar'):
            assert not hasattr(obj, "bar")
            raise RuntimeError('Catch this!')
    assert not hasattr(obj, "bar")

def test_attrrollback_unset_modify():
    obj = SimpleNamespace(foo=42)
    with attrrollback(obj, 'bar'):
        assert not hasattr(obj, "bar")
        obj.bar = [3.14]
    assert not hasattr(obj, "bar")

def test_attrrollback_unset_modify_error():
    obj = SimpleNamespace(foo=42)
    with pytest.raises(RuntimeError, match='Catch this!'):
        with attrrollback(obj, 'bar'):
            assert not hasattr(obj, "bar")
            obj.bar = [3.14]
            raise RuntimeError('Catch this!')
    assert not hasattr(obj, "bar")

def test_attrrollback_no_copy():
    obj = SimpleNamespace(foo={"bar": [1, 2, 3], "quux": ["a", "b", "c"]})
    with attrrollback(obj, "foo"):
        obj.foo["bar"].append(4)
        obj.foo["quux"] = ["x", "y", "z"]
    assert obj.foo == {"bar": [1, 2, 3, 4], "quux": ["x", "y", "z"]}

def test_attrrollback_no_copy_error():
    obj = SimpleNamespace(foo={"bar": [1, 2, 3], "quux": ["a", "b", "c"]})
    with pytest.raises(RuntimeError, match='Catch this!'):
        with attrrollback(obj, "foo"):
            obj.foo["bar"].append(4)
            obj.foo["quux"] = ["x", "y", "z"]
            raise RuntimeError('Catch this!')
    assert obj.foo == {"bar": [1, 2, 3, 4], "quux": ["x", "y", "z"]}

def test_attrrollback_copy():
    obj = SimpleNamespace(foo={"bar": [1, 2, 3], "quux": ["a", "b", "c"]})
    with attrrollback(obj, "foo", copy=True):
        obj.foo["bar"].append(4)
        obj.foo["quux"] = ["x", "y", "z"]
    assert obj.foo == {"bar": [1, 2, 3, 4], "quux": ["a", "b", "c"]}

def test_attrrollback_copy_error():
    obj = SimpleNamespace(foo={"bar": [1, 2, 3], "quux": ["a", "b", "c"]})
    with pytest.raises(RuntimeError, match='Catch this!'):
        with attrrollback(obj, "foo", copy=True):
            obj.foo["bar"].append(4)
            obj.foo["quux"] = ["x", "y", "z"]
            raise RuntimeError('Catch this!')
    assert obj.foo == {"bar": [1, 2, 3, 4], "quux": ["a", "b", "c"]}

@pytest.mark.parametrize('copy', [False, True])
def test_attrrollback_deepcopy(copy):
    obj = SimpleNamespace(foo={"bar": [1, 2, 3], "quux": ["a", "b", "c"]})
    with attrrollback(obj, "foo", copy=copy, deepcopy=True):
        obj.foo["bar"].append(4)
        obj.foo["quux"] = ["x", "y", "z"]
    assert obj.foo == {"bar": [1, 2, 3], "quux": ["a", "b", "c"]}

@pytest.mark.parametrize('copy', [False, True])
def test_attrrollback_deepcopy_error(copy):
    obj = SimpleNamespace(foo={"bar": [1, 2, 3], "quux": ["a", "b", "c"]})
    with pytest.raises(RuntimeError, match='Catch this!'):
        with attrrollback(obj, "foo", copy=copy, deepcopy=True):
            obj.foo["bar"].append(4)
            obj.foo["quux"] = ["x", "y", "z"]
            raise RuntimeError('Catch this!')
    assert obj.foo == {"bar": [1, 2, 3], "quux": ["a", "b", "c"]}
