from types       import SimpleNamespace
from morecontext import attrdel

def test_attrdel():
    obj = SimpleNamespace(foo=42)
    with attrdel(obj, 'foo'):
        assert not hasattr(obj, 'foo')
    assert obj.foo == 42

def test_attrdel_modified():
    obj = SimpleNamespace(foo=42)
    with attrdel(obj, 'foo'):
        assert not hasattr(obj, 'foo')
        obj.foo = [3.14]
    assert obj.foo == 42

def test_attrdel_unset():
    obj = SimpleNamespace(foo=42)
    with attrdel(obj, 'bar'):
        assert not hasattr(obj, "bar")
    assert not hasattr(obj, "bar")

def test_attrdel_unset_modified():
    obj = SimpleNamespace(foo=42)
    with attrdel(obj, 'bar'):
        assert not hasattr(obj, "bar")
        obj.bar = [3.14]
    assert not hasattr(obj, "bar")

def test_attrdel_not_copied():
    x = object()
    obj = SimpleNamespace(foo=x)
    with attrdel(obj, 'foo'):
        assert not hasattr(obj, 'foo')
    assert obj.foo is x
