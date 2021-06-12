from typing import Any, Dict
import pytest
from morecontext import itemdel


def test_itemdel() -> None:
    d = {"foo": 42}
    with itemdel(d, "foo"):
        assert "foo" not in d
    assert d["foo"] == 42


def test_itemdel_error() -> None:
    d = {"foo": 42}
    with pytest.raises(RuntimeError, match="Catch this!"):
        with itemdel(d, "foo"):
            assert "foo" not in d
            raise RuntimeError("Catch this!")
    assert d["foo"] == 42


def test_itemdel_modified() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with itemdel(d, "foo"):
        assert "foo" not in d
        d["foo"] = [3.14]
    assert d["foo"] == 42


def test_itemdel_modified_error() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with pytest.raises(RuntimeError, match="Catch this!"):
        with itemdel(d, "foo"):
            assert "foo" not in d
            d["foo"] = [3.14]
            raise RuntimeError("Catch this!")
    assert d["foo"] == 42


def test_itemdel_unset() -> None:
    d = {"foo": 42}
    with itemdel(d, "bar"):
        assert "bar" not in d
    assert "bar" not in d


def test_itemdel_unset_error() -> None:
    d = {"foo": 42}
    with pytest.raises(RuntimeError, match="Catch this!"):
        with itemdel(d, "bar"):
            assert "bar" not in d
            raise RuntimeError("Catch this!")
    assert "bar" not in d


def test_itemdel_unset_modified() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with itemdel(d, "bar"):
        assert "bar" not in d
        d["bar"] = [3.14]
    assert "bar" not in d


def test_itemdel_unset_modified_error() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with pytest.raises(RuntimeError, match="Catch this!"):
        with itemdel(d, "bar"):
            assert "bar" not in d
            d["bar"] = [3.14]
            raise RuntimeError("Catch this!")
    assert "bar" not in d


def test_itemdel_not_copied() -> None:
    x = object()
    d = {"foo": x}
    with itemdel(d, "foo"):
        assert "foo" not in d
    assert d["foo"] is x


def test_itemdel_not_copied_error() -> None:
    x = object()
    d = {"foo": x}
    with pytest.raises(RuntimeError, match="Catch this!"):
        with itemdel(d, "foo"):
            assert "foo" not in d
            raise RuntimeError("Catch this!")
    assert d["foo"] is x
