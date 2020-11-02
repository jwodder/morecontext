from morecontext import itemset

def test_itemset():
    d = {"foo": 42}
    with itemset(d, 'foo', 'bar'):
        assert d["foo"] == "bar"
    assert d["foo"] == 42

def test_itemset_modified():
    d = {"foo": 42}
    with itemset(d, 'foo', 'bar'):
        assert d["foo"] == "bar"
        d["foo"] = [3.14]
    assert d["foo"] == 42

def test_itemset_delled():
    d = {"foo": 42}
    with itemset(d, 'foo', 'bar'):
        assert d["foo"] == "bar"
        del d["foo"]
    assert d["foo"] == 42

def test_itemset_unset():
    d = {"foo": 42}
    with itemset(d, 'bar', 'quux'):
        assert d["bar"] == "quux"
    assert "bar" not in d

def test_itemset_unset_modified():
    d = {"foo": 42}
    with itemset(d, 'bar', 'quux'):
        assert d["bar"] == "quux"
        d["bar"] = [3.14]
    assert "bar" not in d

def test_itemset_unset_delled():
    d = {"foo": 42}
    with itemset(d, 'bar', 'quux'):
        assert d["bar"] == "quux"
        del d["bar"]
    assert "bar" not in d

def test_itemset_not_copied():
    x = object()
    d = {"foo": x}
    with itemset(d, 'foo', 'bar'):
        assert d["foo"] == "bar"
    assert d["foo"] is x
