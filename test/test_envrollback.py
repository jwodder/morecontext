import os
import pytest
from morecontext import envrollback

ENVVAR = "MORECONTEXT_FOO"


def test_envrollback_nop(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENVVAR, "foo")
    with envrollback(ENVVAR):
        assert os.environ[ENVVAR] == "foo"
    assert os.environ[ENVVAR] == "foo"


def test_envrollback_nop_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENVVAR, "foo")
    with pytest.raises(RuntimeError, match="Catch this!"):
        with envrollback(ENVVAR):
            assert os.environ[ENVVAR] == "foo"
            raise RuntimeError("Catch this!")
    assert os.environ[ENVVAR] == "foo"


def test_envrollback_modify(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENVVAR, "foo")
    with envrollback(ENVVAR):
        assert os.environ[ENVVAR] == "foo"
        os.environ[ENVVAR] = "quux"
    assert os.environ[ENVVAR] == "foo"


def test_envrollback_modify_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENVVAR, "foo")
    with pytest.raises(RuntimeError, match="Catch this!"):
        with envrollback(ENVVAR):
            assert os.environ[ENVVAR] == "foo"
            os.environ[ENVVAR] = "quux"
            raise RuntimeError("Catch this!")
    assert os.environ[ENVVAR] == "foo"


def test_envrollback_del(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENVVAR, "foo")
    with envrollback(ENVVAR):
        assert os.environ[ENVVAR] == "foo"
        del os.environ[ENVVAR]
    assert os.environ[ENVVAR] == "foo"


def test_envrollback_del_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENVVAR, "foo")
    with pytest.raises(RuntimeError, match="Catch this!"):
        with envrollback(ENVVAR):
            assert os.environ[ENVVAR] == "foo"
            del os.environ[ENVVAR]
            raise RuntimeError("Catch this!")
    assert os.environ[ENVVAR] == "foo"


def test_envrollback_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ENVVAR, raising=False)
    with envrollback(ENVVAR):
        assert ENVVAR not in os.environ
    assert ENVVAR not in os.environ


def test_envrollback_unset_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ENVVAR, raising=False)
    with pytest.raises(RuntimeError, match="Catch this!"):
        with envrollback(ENVVAR):
            assert ENVVAR not in os.environ
            raise RuntimeError("Catch this!")
    assert ENVVAR not in os.environ


def test_envrollback_unset_modify(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ENVVAR, raising=False)
    with envrollback(ENVVAR):
        assert ENVVAR not in os.environ
        os.environ[ENVVAR] = "quux"
    assert ENVVAR not in os.environ


def test_envrollback_unset_modify_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ENVVAR, raising=False)
    with pytest.raises(RuntimeError, match="Catch this!"):
        with envrollback(ENVVAR):
            assert ENVVAR not in os.environ
            os.environ[ENVVAR] = "quux"
            raise RuntimeError("Catch this!")
    assert ENVVAR not in os.environ
