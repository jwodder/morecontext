from __future__ import annotations
from morecontext import OpenClosable


class OpenCloser(OpenClosable):
    def __init__(self) -> None:
        self.calls: list[str] = []

    def open(self) -> None:
        self.calls.append("open")

    def close(self) -> None:
        self.calls.append("close")


def test_openclosable() -> None:
    oc = OpenCloser()
    assert oc.calls == []
    with oc as oc2:
        assert oc is oc2
        assert oc.calls == ["open"]
        with oc:
            assert oc.calls == ["open"]
            with oc:
                assert oc.calls == ["open"]
            assert oc.calls == ["open"]
        assert oc.calls == ["open"]
    assert oc.calls == ["open", "close"]
