v0.6.0 (2021-12-17)
-------------------
- `__init__` methods of `OpenClosable` subclasses no longer need to call
  `super().__init__()`

v0.5.0 (2021-11-27)
-------------------
- Support Python 3.10
- Added `OpenClosable` base class for simple reentrant context managers

v0.4.1 (2021-03-15)
-------------------
- Fixed the type annotation on `dirchanged()`

v0.4.0 (2021-03-04)
-------------------
- Added `additem()` for temporarily adding a value to a sequence

v0.3.0 (2020-11-02)
-------------------
- Support Python 3.9
- Gave `attrrollback()` and `itemrollback()` new arguments `copy` and
  `deepcopy` for storing copies of the specified attribute/item

v0.2.0 (2020-10-19)
-------------------
- Added `dirrollback()`, `attrrollback()`, `itemrollback()`, and
  `envrollback()` for undoing changes to a value at the end of a `with` block

v0.1.0 (2020-10-19)
-------------------
Initial release
