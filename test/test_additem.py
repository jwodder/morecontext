import pytest
from morecontext import additem


def test_additem() -> None:
    lst = [1, 2, 3]
    with additem(lst, 42):
        assert lst == [1, 2, 3, 42]
    assert lst == [1, 2, 3]


def test_additem_error() -> None:
    lst = [1, 2, 3]
    with pytest.raises(RuntimeError, match="Catch this!"):
        with additem(lst, 42):
            assert lst == [1, 2, 3, 42]
            raise RuntimeError("Catch this!")
    assert lst == [1, 2, 3]


def test_additem_modified() -> None:
    lst = [1, 2, 3]
    with additem(lst, 42):
        assert lst == [1, 2, 3, 42]
        lst.append(23)
    assert lst == [1, 2, 3, 23]


def test_additem_modified_error() -> None:
    lst = [1, 2, 3]
    with pytest.raises(RuntimeError, match="Catch this!"):
        with additem(lst, 42):
            assert lst == [1, 2, 3, 42]
            lst.append(23)
            raise RuntimeError("Catch this!")
    assert lst == [1, 2, 3, 23]


def test_additem_prepend_same() -> None:
    lst = [1, 2, 3]
    with additem(lst, 42):
        assert lst == [1, 2, 3, 42]
        lst.insert(0, 42)
    assert lst == [42, 1, 2, 3]


def test_additem_prepend_same_error() -> None:
    lst = [1, 2, 3]
    with pytest.raises(RuntimeError, match="Catch this!"):
        with additem(lst, 42):
            assert lst == [1, 2, 3, 42]
            lst.insert(0, 42)
            raise RuntimeError("Catch this!")
    assert lst == [42, 1, 2, 3]


def test_additem_prepend() -> None:
    lst = [1, 2, 3]
    with additem(lst, 42, prepend=True):
        assert lst == [42, 1, 2, 3]
    assert lst == [1, 2, 3]


def test_additem_prepend_error() -> None:
    lst = [1, 2, 3]
    with pytest.raises(RuntimeError, match="Catch this!"):
        with additem(lst, 42, prepend=True):
            assert lst == [42, 1, 2, 3]
            raise RuntimeError("Catch this!")
    assert lst == [1, 2, 3]


def test_additem_prepend_modified() -> None:
    lst = [1, 2, 3]
    with additem(lst, 42, prepend=True):
        assert lst == [42, 1, 2, 3]
        lst.insert(0, 23)
    assert lst == [23, 1, 2, 3]


def test_additem_prepend_modified_error() -> None:
    lst = [1, 2, 3]
    with pytest.raises(RuntimeError, match="Catch this!"):
        with additem(lst, 42, prepend=True):
            assert lst == [42, 1, 2, 3]
            lst.insert(0, 23)
            raise RuntimeError("Catch this!")
    assert lst == [23, 1, 2, 3]


def test_additem_prepend_append_same() -> None:
    lst = [1, 2, 3]
    with additem(lst, 42, prepend=True):
        assert lst == [42, 1, 2, 3]
        lst.append(42)
    assert lst == [1, 2, 3, 42]


def test_additem_prepend_append_same_error() -> None:
    lst = [1, 2, 3]
    with pytest.raises(RuntimeError, match="Catch this!"):
        with additem(lst, 42, prepend=True):
            assert lst == [42, 1, 2, 3]
            lst.append(42)
            raise RuntimeError("Catch this!")
    assert lst == [1, 2, 3, 42]


def test_additem_remove() -> None:
    lst = [1, 2, 3]
    with additem(lst, 42):
        assert lst == [1, 2, 3, 42]
        lst.pop()
    assert lst == [1, 2, 3]


def test_additem_remove_error() -> None:
    lst = [1, 2, 3]
    with pytest.raises(RuntimeError, match="Catch this!"):
        with additem(lst, 42):
            assert lst == [1, 2, 3, 42]
            lst.pop()
            raise RuntimeError("Catch this!")
    assert lst == [1, 2, 3]


def test_additem_prepend_remove() -> None:
    lst = [1, 2, 3]
    with additem(lst, 42, prepend=True):
        assert lst == [42, 1, 2, 3]
        lst.pop(0)
    assert lst == [1, 2, 3]


def test_additem_prepend_remove_error() -> None:
    lst = [1, 2, 3]
    with pytest.raises(RuntimeError, match="Catch this!"):
        with additem(lst, 42, prepend=True):
            assert lst == [42, 1, 2, 3]
            lst.pop(0)
            raise RuntimeError("Catch this!")
    assert lst == [1, 2, 3]


def test_additem_remove_prepend_same() -> None:
    lst = [1, 2, 3]
    with additem(lst, 42):
        assert lst == [1, 2, 3, 42]
        lst.pop()
        lst.insert(0, 42)
    assert lst == [1, 2, 3]


def test_additem_remove_prepend_same_error() -> None:
    lst = [1, 2, 3]
    with pytest.raises(RuntimeError, match="Catch this!"):
        with additem(lst, 42):
            assert lst == [1, 2, 3, 42]
            lst.pop()
            lst.insert(0, 42)
            raise RuntimeError("Catch this!")
    assert lst == [1, 2, 3]


def test_additem_prepend_remove_append_same() -> None:
    lst = [1, 2, 3]
    with additem(lst, 42, prepend=True):
        assert lst == [42, 1, 2, 3]
        lst.pop(0)
        lst.append(42)
    assert lst == [1, 2, 3]


def test_additem_prepend_remove_append_same_error() -> None:
    lst = [1, 2, 3]
    with pytest.raises(RuntimeError, match="Catch this!"):
        with additem(lst, 42, prepend=True):
            assert lst == [42, 1, 2, 3]
            lst.pop(0)
            lst.append(42)
            raise RuntimeError("Catch this!")
    assert lst == [1, 2, 3]
