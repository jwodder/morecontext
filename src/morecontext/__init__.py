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

__version__      = '0.3.0'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'morecontext@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/morecontext'

from   contextlib import contextmanager
import copy as copymod
import os
import sys
from   typing     import Any, TypeVar

if sys.version_info < (3,9):
    from typing import Iterator, MutableMapping
else:
    from collections.abc import Iterator, MutableMapping

__all__ = [
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

K = TypeVar('K')
V = TypeVar('V')

@contextmanager
def dirchanged(dirpath: os.PathLike) -> Iterator[None]:
    """
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
    ``attrdel(obj, name)`` returns a context manager.  On entry, it stores the
    current value of the attribute of ``obj`` with name ``name``, and then it
    unsets that attribute.  On exit, it sets the attribute back to the stored
    value.

    If the given attribute is unset on entry, the context manager will unset it
    on exit.
    """
    with attrrollback(obj, name):
        try:
            delattr(obj, name)
        except AttributeError:
            pass
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
            try:
                delattr(obj, name)
            except AttributeError:
                pass

@contextmanager
def envset(name: str, value: str) -> Iterator[None]:
    """
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
            try:
                del os.environ[name]
            except KeyError:
                pass

@contextmanager
def itemset(d: MutableMapping[K,V], key: K, value: V) -> Iterator[None]:
    """
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
            try:
                del d[key]
            except KeyError:
                pass
