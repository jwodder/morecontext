from   contextlib import contextmanager
import os

@contextmanager
def changing_dir(dirpath):
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
            delattr(obj, name)

@contextmanager
def envset(name, value):
    # Like `attrset()`, but for environment variables
    oldvalue = os.environ.get(name)
    os.environ[name] = value
    try:
        yield
    finally:
        if oldvalue is not None:
            os.environ[name] = oldvalue
        else:
            del os.environ[name]
