"""
Context managers for changing directory, setting attributes/envvars, etc.

Visit <https://github.com/jwodder/morecontext> for more information.
"""

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'morecontext@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/morecontext'

from   contextlib import contextmanager
import os
from   typing     import Any, Generator, MutableMapping, TypeVar

K = TypeVar('K')
V = TypeVar('V')

@contextmanager
def dirchanged(dirpath: os.PathLike) -> Generator[None, None, None]:
    olddir = os.getcwd()
    os.chdir(dirpath)
    try:
        yield
    finally:
        os.chdir(olddir)

@contextmanager
def attrset(obj: Any, name: str, value: Any) -> Generator[None, None, None]:
    """
    ``with attrset(obj, name, value): BLOCK`` will set the ``name`` attribute
    of ``obj`` to ``value`` for the lifetime of ``BLOCK`` and restore the
    original attribute afterwards.
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
def attrdel(obj: Any, name: str) -> Generator[None, None, None]:
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
def envset(name: str, value: str) -> Generator[None, None, None]:
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
def envdel(name: str) -> Generator[None, None, None]:
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
def itemset(d: MutableMapping[K,V], key: K, value: V) -> Generator[None, None, None]:
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
def itemdel(d: MutableMapping[K, Any], key: K) -> Generator[None, None, None]:
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
