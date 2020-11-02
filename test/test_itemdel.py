from morecontext import itemdel

def test_itemdel():
    d = {"foo": 42}
    with itemdel(d, 'foo'):
        assert "foo" not in d
    assert d["foo"] == 42

def test_itemdel_modified():
    d = {"foo": 42}
    with itemdel(d, 'foo'):
        assert "foo" not in d
        d["foo"] = [3.14]
    assert d["foo"] == 42

def test_itemdel_unset():
    d = {"foo": 42}
    with itemdel(d, 'bar'):
        assert "bar" not in d
    assert "bar" not in d

def test_itemdel_unset_modified():
    d = {"foo": 42}
    with itemdel(d, 'bar'):
        assert "bar" not in d
        d["bar"] = [3.14]
    assert "bar" not in d

def test_itemdel_not_copied():
    x = object()
    d = {"foo": x}
    with itemdel(d, 'foo'):
        assert "foo" not in d
    assert d["foo"] is x
