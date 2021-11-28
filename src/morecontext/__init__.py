"""
Context managers for changing directory, setting attributes/envvars, etc.

``morecontext`` provides context managers for some common minor operations:
specifically, changing the current working directory, an object's attribute, a
``dict`` field, or an environment variable and then setting it back afterwards.
Sure, it's easy enough to implement these on your own, but why bother doing
that over & over again when you can let this package do it for you once?

Type annotated!  Fully tested!

Visit <https://github.com/jwodder/morecontext> for more information.
"""

__version__ = "0.5.0"
__author__ = "John Thorvald Wodder II"
__author_email__ = "morecontext@varonathe.org"
__license__ = "MIT"
__url__ = "https://github.com/jwodder/morecontext"

from contextlib import contextmanager, suppress
import copy as copymod
import os
import sys
from types import TracebackType
from typing import Any, Optional, Type, TypeVar, Union

if sys.version_info < (3, 9):
    from typing import Iterator, MutableMapping, MutableSequence
else:
    from collections.abc import Iterator, MutableMapping, MutableSequence

__all__ = [
    "OpenClosable",
    "attrdel",
    "attrrollback",
    "attrset",
    "dirchanged",
    "dirrollback",
    "envdel",
    "envrollback",
    "envset",
    "itemdel",
    "itemrollback",
    "itemset",
]

K = TypeVar("K")
V = TypeVar("V")
OC = TypeVar("OC", bound="OpenClosable")


@contextmanager
def dirchanged(
    dirpath: Union[str, bytes, "os.PathLike[str]", "os.PathLike[bytes]"]
) -> Iterator[None]:
    """
    Temporarily change the current working directory.

    ``dirchanged(dirpath)`` returns a context manager.  On entry, it stores the
    current working directory path and then changes the current directory to
    ``dirpath``.  On exit, it changes the current directory back to the stored
    path.
    """
    with dirrollback():
        os.chdir(dirpath)
        yield


@contextmanager
def dirrollback() -> Iterator[None]:
    """
    .. versionadded:: 0.2.0

    Save & restore the current working directory.

    ``dirrollback()`` returns a context manager that stores the current working
    directory on entry and changes back to that directory on exit.
    """
    olddir = os.getcwd()
    try:
        yield
    finally:
        os.chdir(olddir)


@contextmanager
def attrset(obj: Any, name: str, value: Any) -> Iterator[None]:
    """
    Temporarily change the value of an object's attribute.

    ``attrset(obj, name, value)`` returns a context manager.  On entry, it
    stores the current value of the attribute of ``obj`` with name ``name``,
    and then it sets that attribute to ``value``.  On exit, it sets the
    attribute back to the stored value.

    If the given attribute is unset on entry, the context manager will unset it
    on exit.
    """
    with attrrollback(obj, name):
        setattr(obj, name, value)
        yield


@contextmanager
def attrdel(obj: Any, name: str) -> Iterator[None]:
    """
    Temporarily unset an object's attribute.

    ``attrdel(obj, name)`` returns a context manager.  On entry, it stores the
    current value of the attribute of ``obj`` with name ``name``, and then it
    unsets that attribute.  On exit, it sets the attribute back to the stored
    value.

    If the given attribute is unset on entry, the context manager will unset it
    on exit.
    """
    with attrrollback(obj, name):
        with suppress(AttributeError):
            delattr(obj, name)
        yield


@contextmanager
def attrrollback(
    obj: Any,
    name: str,
    copy: bool = False,
    deepcopy: bool = False,
) -> Iterator[None]:
    """
    .. versionadded:: 0.2.0

    .. versionchanged:: 0.3.0
        ``copy`` and ``deepcopy`` arguments added

    Save & restore the value of an object's attribute.

    ``attrrollback(obj, name)`` returns a context manager that stores the value
    of the attribute of ``obj`` with name ``name`` on entry and sets the
    attribute back to that value on exit.  If the given attribute is unset on
    entry, the context manager will unset it on exit.

    If ``copy`` is true, a shallow copy of the attribute will be saved &
    restored.  If ``deepcopy`` is true, a deep copy of the attribute will be
    saved & restored.  If both options are true, ``deepcopy`` takes precedence.
    """
    try:
        oldvalue = getattr(obj, name)
    except AttributeError:
        oldset = False
    else:
        oldset = True
        if deepcopy:
            oldvalue = copymod.deepcopy(oldvalue)
        elif copy:
            oldvalue = copymod.copy(oldvalue)
    try:
        yield
    finally:
        if oldset:
            setattr(obj, name, oldvalue)
        else:
            with suppress(AttributeError):
                delattr(obj, name)


@contextmanager
def envset(name: str, value: str) -> Iterator[None]:
    """
    Temporarily set an environment variable.

    ``envset(name, value)`` returns a context manager.  On entry, it stores the
    current value of the environment variable ``name``, and then it sets that
    environment variable to ``value``.  On exit, it sets the environment
    variable back to the stored value.

    If the given environment variable is unset on entry, the context manager
    will unset it on exit.
    """
    with envrollback(name):
        os.environ[name] = value
        yield


@contextmanager
def envdel(name: str) -> Iterator[None]:
    """
    Temporarily unset an environment variable.

    ``envdel(name)`` returns a context manager.  On entry, it stores the
    current value of the environment variable ``name``, and then it unsets that
    environment variable.  On exit, it sets the environment variable back to
    the stored value.

    If the given environment variable is unset on entry, the context manager
    will unset it on exit.
    """
    with envrollback(name):
        os.environ.pop(name, None)
        yield


@contextmanager
def envrollback(name: str) -> Iterator[None]:
    """
    .. versionadded:: 0.2.0

    Save & restore the value of an environment variable.

    ``envrollback(name)`` returns a context manager that stores the value of
    the environment variable ``name`` on entry and sets the environment
    variable back to that value on exit.  If the given environment variable is
    unset on entry, the context manager will unset it on exit.
    """
    oldvalue = os.environ.get(name)
    try:
        yield
    finally:
        if oldvalue is not None:
            os.environ[name] = oldvalue
        else:
            with suppress(KeyError):
                del os.environ[name]


@contextmanager
def itemset(d: MutableMapping[K, V], key: K, value: V) -> Iterator[None]:
    """
    Temporarily change the value of a mapping's entry.

    ``itemset(d, key, value)`` returns a context manager.  On entry, it stores
    the current value of ``d[key]``, and then it sets that field to ``value``.
    On exit, it sets the field back to the stored value.

    If the given field is unset on entry, the context manager will unset it
    on exit.
    """
    with itemrollback(d, key):
        d[key] = value
        yield


@contextmanager
def itemdel(d: MutableMapping[K, Any], key: K) -> Iterator[None]:
    """
    Temporarily unset a mapping's entry.

    ``itemdel(d, key)`` returns a context manager.  On entry, it stores the
    current value of ``d[key]``, and then it unsets that field.  On exit, it
    sets the field back to the stored value.

    If the given field is unset on entry, the context manager will unset it
    on exit.
    """
    with itemrollback(d, key):
        d.pop(key, None)
        yield


@contextmanager
def itemrollback(
    d: MutableMapping[K, Any],
    key: K,
    copy: bool = False,
    deepcopy: bool = False,
) -> Iterator[None]:
    """
    .. versionadded:: 0.2.0

    .. versionchanged:: 0.3.0
        ``copy`` and ``deepcopy`` arguments added

    Save & restore the value of a mapping's entry.

    ``itemrollback(d, key)`` returns a context manager that stores the value
    of ``d[key]`` on entry and sets the field back to that value on exit.  If
    the given field is unset on entry, the context manager will unset it on
    exit.

    If ``copy`` is true, a shallow copy of the field will be saved & restored.
    If ``deepcopy`` is true, a deep copy of the field will be saved & restored.
    If both options are true, ``deepcopy`` takes precedence.
    """
    try:
        oldvalue = d[key]
    except KeyError:
        oldset = False
    else:
        oldset = True
        if deepcopy:
            oldvalue = copymod.deepcopy(oldvalue)
        elif copy:
            oldvalue = copymod.copy(oldvalue)
    try:
        yield
    finally:
        if oldset:
            d[key] = oldvalue
        else:
            with suppress(KeyError):
                del d[key]


@contextmanager
def additem(lst: MutableSequence[K], value: K, prepend: bool = False) -> Iterator[None]:
    """
    .. versionadded:: 0.4.0

    Temporarily add a value to a sequence.

    ``additem(lst, value)`` returns a context manager that appends ``value`` to
    the sequence ``lst`` on entry and removes the last item (if any) in ``lst``
    that equals ``value`` on exit.

    If ``prepend`` is true, ``value`` is instead prepended to ``lst`` on entry,
    and the first item in ``lst`` that equals ``value`` is removed on exit.
    """
    if prepend:
        lst.insert(0, value)
    else:
        lst.append(value)
    try:
        yield
    finally:
        if prepend:
            with suppress(ValueError):
                lst.remove(value)
        else:
            for i in range(len(lst) - 1, -1, -1):
                if lst[i] == value:
                    del lst[i]
                    break


class OpenClosable:
    """
    A base class for creating simple reentrant_ context managers.
    `OpenClosable` defines ``__enter__`` and ``__exit__`` methods that keep
    track of the number of nested ``with`` statements in effect and call the
    instance's ``open()`` and ``close()`` methods when entering & exiting the
    outermost ``with``.

    Subclasses should override ``open()`` and/or ``close()`` with the desired
    code to run on entering & exiting the outermost ``with``; the default
    ``open()`` and ``close()`` methods defined by `OpenClosable` do nothing.

    .. note::

        Subclasses' ``__init__()`` methods must call ``super().__init__()`` in
        order to properly initialize `OpenClosable`!

    .. _reentrant: https://docs.python.org/3/library/contextlib.html
                   #reentrant-cms
    """

    def __init__(self) -> None:
        super().__init__()
        self.__depth = 0

    def __enter__(self: OC) -> OC:
        if self.__depth == 0:
            self.open()
        self.__depth += 1
        return self

    def __exit__(
        self,
        _exc_type: Optional[Type[BaseException]],
        _exc_val: Optional[BaseException],
        _exc_tb: Optional[TracebackType],
    ) -> None:
        self.__depth -= 1
        if self.__depth == 0:
            self.close()

    def open(self) -> None:
        ...

    def close(self) -> None:
        ...
