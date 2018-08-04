---
title: Testing python applications with Pytest.
author: ~
date: '2018-07-28'
slug: testing-python-applications-with-pytest
categories: [python]
tags: []
---

# File and class structure

To have your tests executed you need to put them in a *tests* folder. The tests should be grouped in classes where the class name starts with *Test*. Every test is a function of a test class which starts with *test*. Here's an easy example"

```
# content of test_assert1.py
def f():
    return 3

def test_function():
    assert f() == 4
```

As you can see to tests that the output value was indeed what you were expecting, you use the keyword `assert`

# Asserting Errors

Here's an example which asserts that an exception was raised:

```
import pytest

def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

# Fixtures

A fixture is an object that is constructed specifically for the test and is passed as one of the parametres to the test. Here's an example of a database fixture:

```
# content of a/conftest.py
import pytest


class DB(object):
    pass


@pytest.fixture(scope="session")
def db():
    return DB()

def test_a1(db):
    assert 0, db  # to show value
```

Pytest will see that the parametre db of `test_a1` has the same name as the fixture defined previously. The consequence is that pytest will pass the return of the fixture function as that parametre. Furthermore,

```
# content of a/conftest.py
import pytest


class DB(object):
    pass


@pytest.fixture(scope="function")
def db():
    open_db()
    yield DB()
    close_db()

def test_a1(db):
    assert 0, db  # to show value
```

the `yield` keyword will make python create and return the database connection, and then close it, when the *scope* is closed. In the second example a new fixture would be created for each test function. For more on fixtures click [here] (https://docs.pytest.org/en/latest/example/simple.html).

# Mocking

Mocks allow you to replace parts of your production system (which is being tested) with mock objects and make assertions about how they have been used or make them return specified values. Mocking in python is stupidly simple, but that makes it harder to understand. A mock in unit test would be declared so:

```
@patch('module.ClassName2')
@patch('module.ClassName1')
def test(MockClass1, MockClass2):
    module.ClassName1()
    module.ClassName2()
    assert MockClass1 is module.ClassName1
    assert MockClass2 is module.ClassName2
    assert MockClass1.called
    assert MockClass2.called
```

The `patch` decorator allows you to specify which object we are going to replace with a mock. With pytest-mock the process looks like this:

```
import os

class UnixFS:

    @staticmethod
    def rm(filename):
        os.remove(filename)

def test_unix_fs(mocker):
    mocker.patch('os.remove')
    UnixFS.rm('file')
    os.remove.assert_called_once_with('file')
```

Instead of using patch as a decorator, it is called in the function. The `mocker` argument is actually a Mock module fixture, which pytest generates automatically, making the process ridiculously easy. Here's another test which changes the return value of a function the test is testing:

```
class TestMath:
    def test_power(self, mocker):
        mocker.patch.object(math, "multiply")
        math.multiply = 64
        assert math.square(8) = 64
```

# Other notes on mocking

Mocks don't have to substitute functionality in the function, like replacing function outputs. They can also be passed as regular arguments:

```
from mock import Mock

class TestRegister:
    def test_not_under_18(self, mocker):
        form = Mock()
        form.name = "MAX"
        form.lastname = "KEKSIMUS"
        form.age = "17"

        #test will fail because the person is under 18
        #thus not a valid form was submitted
        assert not validate(form)
```

So here, instead of making a complicated form with user data, we just make a mock, and enter the values we know will be used, thus avoiding exporting a lot of crap from other libraries.

# Parametrization

Instead of running a bajillion of tests which basically do the same thing on different input, we can parametrize tests:

```
import pytest
@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 42),
])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

This is pretty nice, because it shrinks the code size of the tests, but it comes at a cost - the tests don't have separate test names. This can be fixed with test ids:

```
@pytest.mark.parametrize(
    'a, b',
    [
        (1, {'Two Scoops of Django': '1.8'}),
        (True, 'Into the Brambles'),
        ('Jason likes cookies', [1, 2, 3]),
        (PYTEST_PLUGIN, 'plugin_template'),
    ], ids=[
        'int and dict',
        'bool and str',
        'str and list',
        'CookiecutterTemplate and str',
    ]
)
def test_foobar(a, b):
    assert True
```

When you run `pytest --verbose` the test id string will be printed along with the string. Still, different groups of tests should be grouped together in different test functions or test classes.

