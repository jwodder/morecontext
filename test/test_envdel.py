import os
from   morecontext import envdel

ENVVAR = "MORECONTEXT_FOO"

def test_envdel(monkeypatch):
    monkeypatch.setenv(ENVVAR, "foo")
    with envdel(ENVVAR):
        assert ENVVAR not in os.environ
    assert os.environ[ENVVAR] == "foo"

def test_envdel_modified(monkeypatch):
    monkeypatch.setenv(ENVVAR, "foo")
    with envdel(ENVVAR):
        assert ENVVAR not in os.environ
        os.environ[ENVVAR] = "quux"
    assert os.environ[ENVVAR] == "foo"

def test_envdel_unset(monkeypatch):
    monkeypatch.delenv(ENVVAR, raising=False)
    with envdel(ENVVAR):
        assert ENVVAR not in os.environ
    assert ENVVAR not in os.environ

def test_envdel_unset_modified(monkeypatch):
    monkeypatch.delenv(ENVVAR, raising=False)
    with envdel(ENVVAR):
        assert ENVVAR not in os.environ
        os.environ[ENVVAR] = "quux"
    assert ENVVAR not in os.environ
