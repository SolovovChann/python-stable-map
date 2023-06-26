# Stable map

This module implements functionality similar to the built-in python class `map` and able to handle exceptions without interrupting the main processing loop.

## Usage

Imagine the situation: there is a set of numbers by which you need to divide the number 100:

```python
from stable_map import StableMap
from stable_map.handlers import LoggingHandler


def divide_100_to(number: int) -> float:
    return 100 // number


sequence = [4, 1, 2, 0, 5, 8]
stable_map = StableMap(divide_100_to, sequence, [
    LoggingHandler(),
])

print(list(stable_map))
```

When the iterator reaches the fourth value in the sequence (zero), a `ZeroDivisionError` exception will be raised. It does not stop the processing of the remaining elements of the sequence, but will be logged.

## Creating Your Own Handlers

If you need to handle an element in a certain way, during the processing of which an exception was thrown, you can create your own handler class. To do this, import the `ErrorHandler` class from the `stable_map.handler` module and extend the `handle` method:

```python
from stable_map.context import ErrorContext, ExceptionType, T
from stable_map.handler import ErrorHandler


class MyHandler(ErrorHandler[T, ExceptionType]):
    def handle(self, context: ErrorContext[T, ExceptionType]) -> None:
        # do some cool stuff
        ...
```

You can specify the type of sequence elements that the handler can work with. If you try to use a handler with an inappropriate type, a static type analyzer (for example, pylance) will issue a warning:

```python
class MyIntHandler(ErrorHandler[int, ExceptionType]):
    def handle(self, context: ErrorContext[int, ExceptionType]) -> None:
        ...

class MyStrHandler(ErrorHandler[str, ExceptionType]):
    def handle(self, context: ErrorContext[str, ExceptionType]) -> None:
        ...


sequence = [1, 2, 3, 4, 5]
stable_map = StableMap(divide_100_to, sequence, [
    LoggingHandler(), # ok
    MyIntHandler(), # ok
    MyStrHandler(), # "str" is incompatible with "int"
])
```

You can also specify the type of exceptions that your handler can handle:

```python
class CustomError(Exception):
    def __init__(self, name: str, *args: object) -> None:
        super().__init__(*args)
        self.name = name


class MyIntHandler(ErrorHandler[int, CustomError]):
    def handle(self, context: ErrorContext[int, CustomError]) -> None:
        print(context.exception.name)


sequence = [1, 2, 3, 4, 5]
stable_map = StableMap(divide_100_to, sequence, [
    LoggingHandler(),
    MyIntHandler(exceptions=[CustomError]),
])
```

## Using Handlers for Specific Exceptions

Handlers can be configured to handle specific exceptions. The "exceptions" field of the `ErrorHandler` class defines the types of exceptions that the handler will respond to, and the "ignore" field defines the types of exceptions that will be ignored.

**Important!** The exception types in the `ErrorHandler.exceptions` field are **covariant**, while those in the `ErrorHandler.ignore` field are **invariant**.

### Examples

Let's imagine that the exception scheme looks like this:

```
BaseException
├── A
├── B
├── C
│   ├── C1
│   ├── C2
│   ├── C3
│   │   ├── C3_1
│   │   ├── C3_2
```

There are some examples of different exception configurations:

```python
# all the BaseException class children
exceptions = [BaseException]
ignore = []

# all the C class children:
# C1, C2, C3, C3_1, C3_2
exceptions = [C]
ignore = []

# all the BaseException class children except B
exceptions = [BaseException]
ignore = [B]

# all the BaseException children except C
# but including C1, С2, C3, C3_1, C3_2
exceptions = [BaseException]
ignore = [C]
```

