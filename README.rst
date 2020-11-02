.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://travis-ci.com/jwodder/morecontext.svg?branch=master
    :target: https://travis-ci.com/jwodder/morecontext

.. image:: https://codecov.io/gh/jwodder/morecontext/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/morecontext

.. image:: https://img.shields.io/pypi/pyversions/morecontext.svg
    :target: https://pypi.org/project/morecontext/

.. image:: https://img.shields.io/github/license/jwodder/morecontext.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/morecontext>`_
| `PyPI <https://pypi.org/project/morecontext/>`_
| `Issues <https://github.com/jwodder/morecontext/issues>`_
| `Changelog <https://github.com/jwodder/morecontext/blob/master/CHANGELOG.md>`_

``morecontext`` provides context managers for some common minor operations:
specifically, changing the current working directory, an object's attribute, a
``dict`` field, or an environment variable and then setting it back afterwards.
Sure, it's easy enough to implement these on your own, but why bother doing
that over & over again when you can let this package do it for you once?

Type annotated!  Fully tested!


Installation
============
``morecontext`` requires Python 3.6 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install
``morecontext``::

    python3 -m pip install morecontext


Examples
========

>>> import os
>>> import morecontext
>>> os.getcwd()
'/some/dir'
>>> with morecontext.dirchanged('/some/other/dir'):
...     # Now we're in /some/other/dir
...     os.getcwd()
... 
'/some/other/dir'
>>> # Out of the `with`, back to /some/dir
>>> os.getcwd()
'/some/dir'

>>> d = {"foo": 42}
>>> with morecontext.itemset(d, "foo", "bar"):
...     # d["foo"] == "bar" in here
...     d["foo"]
...     # If we change d["foo"] in here, it'll still be set back to 42 on exit
...     d["foo"] = 3.14
... 
'bar'
>>> # Out of the `with`, it's back to 42
>>> d["foo"]
42


API
===

All of the context managers in ``morecontext`` are defined with
``contextlib.contextmanager``, so they can be used as function decorators as
well.  All context managers return ``None`` on entry, so there's no point in
writing "``with dirchanged(path) as foo:``"; just do "``with
dirchanged(path):``".

These functions are not thread-safe.

.. code:: python

    dirchanged(dirpath: os.PathLike) -> ContextManager[None]

``dirchanged(dirpath)`` returns a context manager.  On entry, it stores the
current working directory path and then changes the current directory to
``dirpath``.  On exit, it changes the current directory back to the stored
path.

.. code:: python

    dirrollback() -> ContextManager[None]

``dirrollback()`` returns a context manager that stores the current working
directory on entry and changes back to that directory on exit.

.. code:: python

    attrset(obj: Any, name: str, value: Any) -> ContextManager[None]

``attrset(obj, name, value)`` returns a context manager.  On entry, it stores
the current value of the attribute of ``obj`` with name ``name``, and then it
sets that attribute to ``value``.  On exit, it sets the attribute back to the
stored value.

If the given attribute is unset on entry, the context manager will unset it on
exit.

.. code:: python

    attrdel(obj: Any, name: str) -> ContextManager[None]

``attrdel(obj, name)`` returns a context manager.  On entry, it stores the
current value of the attribute of ``obj`` with name ``name``, and then it
unsets that attribute.  On exit, it sets the attribute back to the stored
value.

If the given attribute is unset on entry, the context manager will unset it on
exit.

.. code:: python

    attrrollback(obj: Any, name: str, copy: bool = False, deepcopy: bool = False) -> ContextManager[None]

``attrrollback(obj, name)`` returns a context manager that stores the value of
the attribute of ``obj`` with name ``name`` on entry and sets the attribute
back to that value on exit.  If the given attribute is unset on entry, the
context manager will unset it on exit.

If ``copy`` is true, a shallow copy of the attribute will be saved & restored.
If ``deepcopy`` is true, a deep copy of the attribute will be saved & restored.
If both options are true, ``deepcopy`` takes precedence.

.. code:: python

    itemset(d: MutableMapping[K,V], key: K, value: V) -> ContextManager[None]

``itemset(d, key, value)`` returns a context manager.  On entry, it stores the
current value of ``d[key]``, and then it sets that field to ``value``.  On
exit, it sets the field back to the stored value.

If the given field is unset on entry, the context manager will unset it on
exit.

.. code:: python

    itemdel(d: MutableMapping[K, Any], key: K) -> ContextManager[None]

``itemdel(d, key)`` returns a context manager.  On entry, it stores the current
value of ``d[key]``, and then it unsets that field.  On exit, it sets the field
back to the stored value.

If the given field is unset on entry, the context manager will unset it on
exit.

.. code:: python

    itemrollback(d: MutableMapping[K, Any], key: K, copy: bool = False, deepcopy: bool = False) -> ContextManager[None]

``itemrollback(d, key)`` returns a context manager that stores the value of
``d[key]`` on entry and sets the field back to that value on exit.  If the
given field is unset on entry, the context manager will unset it on exit.

If ``copy`` is true, a shallow copy of the field will be saved & restored.  If
``deepcopy`` is true, a deep copy of the field will be saved & restored.  If
both options are true, ``deepcopy`` takes precedence.

.. code:: python

    envset(name: str, value: str) -> ContextManager[None]

``envset(name, value)`` returns a context manager.  On entry, it stores the
current value of the environment variable ``name``, and then it sets that
environment variable to ``value``.  On exit, it sets the environment variable
back to the stored value.

If the given environment variable is unset on entry, the context manager will
unset it on exit.

.. code:: python

    envdel(name: str) -> ContextManager[None]

``envdel(name)`` returns a context manager.  On entry, it stores the current
value of the environment variable ``name``, and then it unsets that environment
variable.  On exit, it sets the environment variable back to the stored value.

If the given environment variable is unset on entry, the context manager will
unset it on exit.

.. code:: python

    envrollback(name: str) -> ContextManager[None]

``envrollback(name)`` returns a context manager that stores the value of the
environment variable ``name`` on entry and sets the environment variable back
to that value on exit.  If the given environment variable is unset on entry,
the context manager will unset it on exit.
