from typing import Any, Dict
import pytest
from morecontext import itemset


def test_itemset() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with itemset(d, "foo", "bar"):
        assert d["foo"] == "bar"
    assert d["foo"] == 42


def test_itemset_error() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with pytest.raises(RuntimeError, match="Catch this!"):
        with itemset(d, "foo", "bar"):
            assert d["foo"] == "bar"
            raise RuntimeError("Catch this!")
    assert d["foo"] == 42


def test_itemset_modified() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with itemset(d, "foo", "bar"):
        assert d["foo"] == "bar"
        d["foo"] = [3.14]
    assert d["foo"] == 42


def test_itemset_modified_error() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with pytest.raises(RuntimeError, match="Catch this!"):
        with itemset(d, "foo", "bar"):
            assert d["foo"] == "bar"
            d["foo"] = [3.14]
            raise RuntimeError("Catch this!")
    assert d["foo"] == 42


def test_itemset_delled() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with itemset(d, "foo", "bar"):
        assert d["foo"] == "bar"
        del d["foo"]
    assert d["foo"] == 42


def test_itemset_delled_error() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with pytest.raises(RuntimeError, match="Catch this!"):
        with itemset(d, "foo", "bar"):
            assert d["foo"] == "bar"
            del d["foo"]
            raise RuntimeError("Catch this!")
    assert d["foo"] == 42


def test_itemset_unset() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with itemset(d, "bar", "quux"):
        assert d["bar"] == "quux"
    assert "bar" not in d


def test_itemset_unset_error() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with pytest.raises(RuntimeError, match="Catch this!"):
        with itemset(d, "bar", "quux"):
            assert d["bar"] == "quux"
            raise RuntimeError("Catch this!")
    assert "bar" not in d


def test_itemset_unset_modified() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with itemset(d, "bar", "quux"):
        assert d["bar"] == "quux"
        d["bar"] = [3.14]
    assert "bar" not in d


def test_itemset_unset_modified_error() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with pytest.raises(RuntimeError, match="Catch this!"):
        with itemset(d, "bar", "quux"):
            assert d["bar"] == "quux"
            d["bar"] = [3.14]
            raise RuntimeError("Catch this!")
    assert "bar" not in d


def test_itemset_unset_delled() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with itemset(d, "bar", "quux"):
        assert d["bar"] == "quux"
        del d["bar"]
    assert "bar" not in d


def test_itemset_unset_delled_error() -> None:
    d: Dict[str, Any] = {"foo": 42}
    with pytest.raises(RuntimeError, match="Catch this!"):
        with itemset(d, "bar", "quux"):
            assert d["bar"] == "quux"
            del d["bar"]
            raise RuntimeError("Catch this!")
    assert "bar" not in d


def test_itemset_not_copied() -> None:
    x = object()
    d: Dict[str, Any] = {"foo": x}
    with itemset(d, "foo", "bar"):
        assert d["foo"] == "bar"
    assert d["foo"] is x


def test_itemset_not_copied_error() -> None:
    x = object()
    d: Dict[str, Any] = {"foo": x}
    with pytest.raises(RuntimeError, match="Catch this!"):
        with itemset(d, "foo", "bar"):
            assert d["foo"] == "bar"
            raise RuntimeError("Catch this!")
    assert d["foo"] is x
