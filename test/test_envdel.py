import os
import pytest
from morecontext import envdel

ENVVAR = "MORECONTEXT_FOO"


def test_envdel(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENVVAR, "foo")
    with envdel(ENVVAR):
        assert ENVVAR not in os.environ
    assert os.environ[ENVVAR] == "foo"


def test_envdel_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENVVAR, "foo")
    with pytest.raises(RuntimeError, match="Catch this!"):
        with envdel(ENVVAR):
            assert ENVVAR not in os.environ
            raise RuntimeError("Catch this!")
    assert os.environ[ENVVAR] == "foo"


def test_envdel_modified(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENVVAR, "foo")
    with envdel(ENVVAR):
        assert ENVVAR not in os.environ
        os.environ[ENVVAR] = "quux"
    assert os.environ[ENVVAR] == "foo"


def test_envdel_modified_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENVVAR, "foo")
    with pytest.raises(RuntimeError, match="Catch this!"):
        with envdel(ENVVAR):
            assert ENVVAR not in os.environ
            os.environ[ENVVAR] = "quux"
            raise RuntimeError("Catch this!")
    assert os.environ[ENVVAR] == "foo"


def test_envdel_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ENVVAR, raising=False)
    with envdel(ENVVAR):
        assert ENVVAR not in os.environ
    assert ENVVAR not in os.environ


def test_envdel_unset_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ENVVAR, raising=False)
    with pytest.raises(RuntimeError, match="Catch this!"):
        with envdel(ENVVAR):
            assert ENVVAR not in os.environ
            raise RuntimeError("Catch this!")
    assert ENVVAR not in os.environ


def test_envdel_unset_modified(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ENVVAR, raising=False)
    with envdel(ENVVAR):
        assert ENVVAR not in os.environ
        os.environ[ENVVAR] = "quux"
    assert ENVVAR not in os.environ


def test_envdel_unset_modified_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ENVVAR, raising=False)
    with pytest.raises(RuntimeError, match="Catch this!"):
        with envdel(ENVVAR):
            assert ENVVAR not in os.environ
            os.environ[ENVVAR] = "quux"
            raise RuntimeError("Catch this!")
    assert ENVVAR not in os.environ
