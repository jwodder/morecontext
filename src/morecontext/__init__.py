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

__version__      = '0.1.0'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'morecontext@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/morecontext'

from   contextlib import contextmanager
import os
import sys
from   typing     import Any, TypeVar

if sys.version_info < (3,9):
    from typing import Iterator, MutableMapping
else:
    from collections.abc import Iterator, MutableMapping

__all__ = [
    "attrdel",
    "attrset",
    "dirchanged",
    "envdel",
    "envset",
    "itemdel",
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
    olddir = os.getcwd()
    os.chdir(dirpath)
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
    try:
        oldvalue = getattr(obj, name)
        oldset = True
    except AttributeError:
        oldset = False
    setattr(obj, name, value)
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
def attrdel(obj: Any, name: str) -> Iterator[None]:
    """
    ``attrdel(obj, name)`` returns a context manager.  On entry, it stores the
    current value of the attribute of ``obj`` with name ``name``, and then it
    unsets that attribute.  On exit, it sets the attribute back to the stored
    value.

    If the given attribute is unset on entry, the context manager will unset it
    on exit.
    """
    try:
        oldvalue = getattr(obj, name)
        oldset = True
    except AttributeError:
        oldset = False
    else:
        delattr(obj, name)
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
    oldvalue = os.environ.get(name)
    os.environ[name] = value
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
def envdel(name: str) -> Iterator[None]:
    """
    ``envdel(name)`` returns a context manager.  On entry, it stores the
    current value of the environment variable ``name``, and then it unsets that
    environment variable.  On exit, it sets the environment variable back to
    the stored value.

    If the given environment variable is unset on entry, the context manager
    will unset it on exit.
    """
    oldvalue = os.environ.get(name)
    try:
        del os.environ[name]
    except KeyError:
        pass
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
    try:
        oldvalue = d[key]
        oldset = True
    except KeyError:
        oldset = False
    d[key] = value
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

@contextmanager
def itemdel(d: MutableMapping[K, Any], key: K) -> Iterator[None]:
    """
    ``itemdel(d, key)`` returns a context manager.  On entry, it stores the
    current value of ``d[key]``, and then it unsets that field.  On exit, it
    sets the field back to the stored value.

    If the given field is unset on entry, the context manager will unset it
    on exit.
    """
    try:
        oldvalue = d[key]
        oldset = True
    except KeyError:
        oldset = False
    else:
        del d[key]
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
