import os
from   morecontext import envrollback

ENVVAR = "MORECONTEXT_FOO"

def test_envrollback_nop(monkeypatch):
    monkeypatch.setenv(ENVVAR, "foo")
    with envrollback(ENVVAR):
        assert os.environ[ENVVAR] == "foo"
    assert os.environ[ENVVAR] == "foo"

def test_envrollback_modify(monkeypatch):
    monkeypatch.setenv(ENVVAR, "foo")
    with envrollback(ENVVAR):
        assert os.environ[ENVVAR] == "foo"
        os.environ[ENVVAR] = "quux"
    assert os.environ[ENVVAR] == "foo"

def test_envrollback_del(monkeypatch):
    monkeypatch.setenv(ENVVAR, "foo")
    with envrollback(ENVVAR):
        assert os.environ[ENVVAR] == "foo"
        del os.environ[ENVVAR]
    assert os.environ[ENVVAR] == "foo"

def test_envrollback_unset(monkeypatch):
    monkeypatch.delenv(ENVVAR, raising=False)
    with envrollback(ENVVAR):
        assert ENVVAR not in os.environ
    assert ENVVAR not in os.environ

def test_envrollback_unset_modify(monkeypatch):
    monkeypatch.delenv(ENVVAR, raising=False)
    with envrollback(ENVVAR):
        assert ENVVAR not in os.environ
        os.environ[ENVVAR] = "quux"
    assert ENVVAR not in os.environ
