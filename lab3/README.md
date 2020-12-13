#Py2sqlite3
____

Py2sqlite3 is a library that facilitates the communication between python objects and sqlite3 databases

____

## Installation

https://pypi.org/project/py2sqlite3/

`pip install py2sqlite3`
____

## Command line usage (only to run test):

python -m py2sqlite3

____

## Usage as library

### Example

```
from py2sqlite3 import Py2sqlite3

class Foo:
    bar = 0

class Foo2(Foo):
    pass

py2sql = Py2sqlite3()

py2sql.db_connect('test.db')
py2sql.save_class(Foo)              # saves class Foo
py2sql.save_class_hierarchy(Foo)    # saves Foo and Foo2
py2sql.save_object(Foo())           # saves object of class Foo

py2sql.delete_class(Foo)            # deletes class Foo
py2sql.delete_class_hierarchy(Foo)  # deletes Foo and Foo2
py2sql.delete_object(Foo())         # deletes object of class Foo

py2sql.db_disconnect()
```
