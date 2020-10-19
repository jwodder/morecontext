from types       import SimpleNamespace
from morecontext import attrrollback

def test_attrrollback_nop():
    obj = SimpleNamespace(foo=42)
    with attrrollback(obj, 'foo'):
        assert obj.foo == 42
    assert obj.foo == 42

def test_attrrollback_modify():
    obj = SimpleNamespace(foo=42)
    with attrrollback(obj, 'foo'):
        assert obj.foo == 42
        obj.foo = [3.14]
    assert obj.foo == 42

def test_attrrollback_del():
    obj = SimpleNamespace(foo=42)
    with attrrollback(obj, 'foo'):
        assert obj.foo == 42
        del obj.foo
    assert obj.foo == 42

def test_attrrollback_unset():
    obj = SimpleNamespace(foo=42)
    with attrrollback(obj, 'bar'):
        assert not hasattr(obj, "bar")
    assert not hasattr(obj, "bar")

def test_attrrollback_unset_modify():
    obj = SimpleNamespace(foo=42)
    with attrrollback(obj, 'bar'):
        assert not hasattr(obj, "bar")
        obj.bar = [3.14]
    assert not hasattr(obj, "bar")
