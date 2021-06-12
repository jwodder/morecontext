from types import SimpleNamespace
import pytest
from morecontext import attrdel


def test_attrdel() -> None:
    obj = SimpleNamespace(foo=42)
    with attrdel(obj, "foo"):
        assert not hasattr(obj, "foo")
    assert obj.foo == 42


def test_attrdel_error() -> None:
    obj = SimpleNamespace(foo=42)
    with pytest.raises(RuntimeError, match="Catch this!"):
        with attrdel(obj, "foo"):
            assert not hasattr(obj, "foo")
            raise RuntimeError("Catch this!")
    assert obj.foo == 42


def test_attrdel_modified() -> None:
    obj = SimpleNamespace(foo=42)
    with attrdel(obj, "foo"):
        assert not hasattr(obj, "foo")
        obj.foo = [3.14]
    assert obj.foo == 42  # type: ignore[comparison-overlap]


def test_attrdel_modified_error() -> None:
    obj = SimpleNamespace(foo=42)
    with pytest.raises(RuntimeError, match="Catch this!"):
        with attrdel(obj, "foo"):
            assert not hasattr(obj, "foo")
            obj.foo = [3.14]
            raise RuntimeError("Catch this!")
    assert obj.foo == 42


def test_attrdel_unset() -> None:
    obj = SimpleNamespace(foo=42)
    with attrdel(obj, "bar"):
        assert not hasattr(obj, "bar")
    assert not hasattr(obj, "bar")


def test_attrdel_unset_error() -> None:
    obj = SimpleNamespace(foo=42)
    with pytest.raises(RuntimeError, match="Catch this!"):
        with attrdel(obj, "bar"):
            assert not hasattr(obj, "bar")
            raise RuntimeError("Catch this!")
    assert not hasattr(obj, "bar")


def test_attrdel_unset_modified() -> None:
    obj = SimpleNamespace(foo=42)
    with attrdel(obj, "bar"):
        assert not hasattr(obj, "bar")
        obj.bar = [3.14]
    assert not hasattr(obj, "bar")


def test_attrdel_unset_modified_error() -> None:
    obj = SimpleNamespace(foo=42)
    with pytest.raises(RuntimeError, match="Catch this!"):
        with attrdel(obj, "bar"):
            assert not hasattr(obj, "bar")
            obj.bar = [3.14]
            raise RuntimeError("Catch this!")
    assert not hasattr(obj, "bar")


def test_attrdel_not_copied() -> None:
    x = object()
    obj = SimpleNamespace(foo=x)
    with attrdel(obj, "foo"):
        assert not hasattr(obj, "foo")
    assert obj.foo is x


def test_attrdel_not_copied_error() -> None:
    x = object()
    obj = SimpleNamespace(foo=x)
    with pytest.raises(RuntimeError, match="Catch this!"):
        with attrdel(obj, "foo"):
            assert not hasattr(obj, "foo")
            raise RuntimeError("Catch this!")
    assert obj.foo is x
