import os
import pytest
from   morecontext import envset

ENVVAR = "MORECONTEXT_FOO"

def test_envset(monkeypatch):
    monkeypatch.setenv(ENVVAR, "foo")
    with envset(ENVVAR, "bar"):
        assert os.environ[ENVVAR] == "bar"
    assert os.environ[ENVVAR] == "foo"

def test_envset_error(monkeypatch):
    monkeypatch.setenv(ENVVAR, "foo")
    with pytest.raises(RuntimeError, match='Catch this!'):
        with envset(ENVVAR, "bar"):
            assert os.environ[ENVVAR] == "bar"
            raise RuntimeError('Catch this!')
    assert os.environ[ENVVAR] == "foo"

def test_envset_modified(monkeypatch):
    monkeypatch.setenv(ENVVAR, "foo")
    with envset(ENVVAR, "bar"):
        assert os.environ[ENVVAR] == "bar"
        os.environ[ENVVAR] = "quux"
    assert os.environ[ENVVAR] == "foo"

def test_envset_modified_error(monkeypatch):
    monkeypatch.setenv(ENVVAR, "foo")
    with pytest.raises(RuntimeError, match='Catch this!'):
        with envset(ENVVAR, "bar"):
            assert os.environ[ENVVAR] == "bar"
            os.environ[ENVVAR] = "quux"
            raise RuntimeError('Catch this!')
    assert os.environ[ENVVAR] == "foo"

def test_envset_delled(monkeypatch):
    monkeypatch.setenv(ENVVAR, "foo")
    with envset(ENVVAR, "bar"):
        assert os.environ[ENVVAR] == "bar"
        del os.environ[ENVVAR]
    assert os.environ[ENVVAR] == "foo"

def test_envset_delled_error(monkeypatch):
    monkeypatch.setenv(ENVVAR, "foo")
    with pytest.raises(RuntimeError, match='Catch this!'):
        with envset(ENVVAR, "bar"):
            assert os.environ[ENVVAR] == "bar"
            del os.environ[ENVVAR]
            raise RuntimeError('Catch this!')
    assert os.environ[ENVVAR] == "foo"

def test_envset_unset(monkeypatch):
    monkeypatch.delenv(ENVVAR, raising=False)
    with envset(ENVVAR, "bar"):
        assert os.environ[ENVVAR] == "bar"
    assert ENVVAR not in os.environ

def test_envset_unset_error(monkeypatch):
    monkeypatch.delenv(ENVVAR, raising=False)
    with pytest.raises(RuntimeError, match='Catch this!'):
        with envset(ENVVAR, "bar"):
            assert os.environ[ENVVAR] == "bar"
            raise RuntimeError('Catch this!')
    assert ENVVAR not in os.environ

def test_envset_unset_modified(monkeypatch):
    monkeypatch.delenv(ENVVAR, raising=False)
    with envset(ENVVAR, "bar"):
        assert os.environ[ENVVAR] == "bar"
        os.environ[ENVVAR] = "quux"
    assert ENVVAR not in os.environ

def test_envset_unset_modified_error(monkeypatch):
    monkeypatch.delenv(ENVVAR, raising=False)
    with pytest.raises(RuntimeError, match='Catch this!'):
        with envset(ENVVAR, "bar"):
            assert os.environ[ENVVAR] == "bar"
            os.environ[ENVVAR] = "quux"
            raise RuntimeError('Catch this!')
    assert ENVVAR not in os.environ

def test_envset_unset_delled(monkeypatch):
    monkeypatch.delenv(ENVVAR, raising=False)
    with envset(ENVVAR, "bar"):
        assert os.environ[ENVVAR] == "bar"
        del os.environ[ENVVAR]
    assert ENVVAR not in os.environ

def test_envset_unset_delled_error(monkeypatch):
    monkeypatch.delenv(ENVVAR, raising=False)
    with pytest.raises(RuntimeError, match='Catch this!'):
        with envset(ENVVAR, "bar"):
            assert os.environ[ENVVAR] == "bar"
            del os.environ[ENVVAR]
            raise RuntimeError('Catch this!')
    assert ENVVAR not in os.environ
