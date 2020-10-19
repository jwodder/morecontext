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

@contextmanager
def dirchanged(dirpath):
    olddir = os.getcwd()
    os.chdir(dirpath)
    try:
        yield
    finally:
        os.chdir(olddir)

@contextmanager
def attrset(obj, name, value):
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
def envset(name, value):
    oldvalue = os.environ.get(name)
    os.environ[name] = value
    try:
        yield
    finally:
        if oldvalue is not None:
            os.environ[name] = oldvalue
        else:
            del os.environ[name]
