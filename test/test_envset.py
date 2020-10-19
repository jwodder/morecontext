import os
from   morecontext import envset

def test_envset(monkeypatch):
    monkeypatch.setenv("MORECONTEXT_FOO", "foo")
    with envset("MORECONTEXT_FOO", "bar"):
        assert os.environ["MORECONTEXT_FOO"] == "bar"
    assert os.environ["MORECONTEXT_FOO"] == "foo"

def test_envset_modified(monkeypatch):
    monkeypatch.setenv("MORECONTEXT_FOO", "foo")
    with envset("MORECONTEXT_FOO", "bar"):
        assert os.environ["MORECONTEXT_FOO"] == "bar"
        os.environ["MORECONTXET_FOO"] = "quux"
    assert os.environ["MORECONTEXT_FOO"] == "foo"

def test_envset_delled(monkeypatch):
    monkeypatch.setenv("MORECONTEXT_FOO", "foo")
    with envset("MORECONTEXT_FOO", "bar"):
        assert os.environ["MORECONTEXT_FOO"] == "bar"
        del os.environ["MORECONTXET_FOO"]
    assert os.environ["MORECONTEXT_FOO"] == "foo"

def test_envset_unset(monkeypatch):
    monkeypatch.delenv("MORECONTEXT_FOO", raising=False)
    with envset("MORECONTEXT_FOO", "bar"):
        assert os.environ["MORECONTEXT_FOO"] == "bar"
    assert "MORECONTEXT_FOO" not in os.environ

def test_envset_unset_modified(monkeypatch):
    monkeypatch.delenv("MORECONTEXT_FOO", raising=False)
    with envset("MORECONTEXT_FOO", "bar"):
        assert os.environ["MORECONTEXT_FOO"] == "bar"
        os.environ["MORECONTXET_FOO"] = "quux"
    assert "MORECONTEXT_FOO" not in os.environ

def test_envset_unset_delled(monkeypatch):
    monkeypatch.delenv("MORECONTEXT_FOO", raising=False)
    with envset("MORECONTEXT_FOO", "bar"):
        assert os.environ["MORECONTEXT_FOO"] == "bar"
        del os.environ["MORECONTXET_FOO"]
    assert "MORECONTEXT_FOO" not in os.environ
