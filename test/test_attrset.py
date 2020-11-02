from types       import SimpleNamespace
from morecontext import attrset

def test_attrset():
    obj = SimpleNamespace(foo=42)
    with attrset(obj, 'foo', 'bar'):
        assert obj.foo == "bar"
    assert obj.foo == 42

def test_attrset_modified():
    obj = SimpleNamespace(foo=42)
    with attrset(obj, 'foo', 'bar'):
        assert obj.foo == "bar"
        obj.foo = [3.14]
    assert obj.foo == 42

def test_attrset_delled():
    obj = SimpleNamespace(foo=42)
    with attrset(obj, 'foo', 'bar'):
        assert obj.foo == "bar"
        del obj.foo
    assert obj.foo == 42

def test_attrset_unset():
    obj = SimpleNamespace(foo=42)
    with attrset(obj, 'bar', 'quux'):
        assert obj.bar == "quux"
    assert not hasattr(obj, "bar")

def test_attrset_unset_modified():
    obj = SimpleNamespace(foo=42)
    with attrset(obj, 'bar', 'quux'):
        assert obj.bar == "quux"
        obj.bar = [3.14]
    assert not hasattr(obj, "bar")

def test_attrset_unset_delled():
    obj = SimpleNamespace(foo=42)
    with attrset(obj, 'bar', 'quux'):
        assert obj.bar == "quux"
        del obj.bar
    assert not hasattr(obj, "bar")

def test_attrset_not_copied():
    x = object()
    obj = SimpleNamespace(foo=x)
    with attrset(obj, 'foo', 'bar'):
        assert obj.foo == "bar"
    assert obj.foo is x
