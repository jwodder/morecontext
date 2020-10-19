from morecontext import itemrollback

def test_itemrollback_nop():
    d = {"foo": 42}
    with itemrollback(d, 'foo'):
        assert d["foo"] == 42
    assert d["foo"] == 42

def test_itemrollback_modify():
    d = {"foo": 42}
    with itemrollback(d, 'foo'):
        assert d["foo"] == 42
        d["foo"] = [3.14]
    assert d["foo"] == 42

def test_itemrollback_del():
    d = {"foo": 42}
    with itemrollback(d, 'foo'):
        assert d["foo"] == 42
        del d["foo"]
    assert d["foo"] == 42

def test_itemrollback_unset():
    d = {"foo": 42}
    with itemrollback(d, 'bar'):
        assert "bar" not in d
    assert "bar" not in d

def test_itemrollback_unset_modify():
    d = {"foo": 42}
    with itemrollback(d, 'bar'):
        assert "bar" not in d
        d["bar"] = [3.14]
    assert "bar" not in d
