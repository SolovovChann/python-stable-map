# Stable map

A tool similar to the built-in python `map`, but reacting to exceptions that occur.

## Usage

### General example

```python
from pathlib import Path

from stable_map import StableMap
from stable_map.handlers import LoggingHandler

dest = Path('output')

sequence = [4, 1, 2, 0, 5, 8]
stable_map = StableMap(lambda i: 100 // i, sequence, [
    LoggingHandler([Exception], []),
])

for index, integer in enumerate(stable_map, 1):
    print('%i. %i' % (index, integer))
```

In this example, when iterator reaches the third element of the sequence and tries to do division by zero, an exception will be logged and processing will not stop.

### Customizing handlers for specific exceptions

Each of the handlers can be flexibly configured for specific exceptions during initialization. The `exceptions` field defines the types of exceptions that the handler will respond to, and the `ignore` field defines the types of exceptions that will be skipped.

> **Note**
> The `exceptions` types are `covariant` and the `ignore` types are `invariant`.

#### Respond to all exception types

```python
ErrorHandler([Exception], [])
```

#### React to all types of exceptions except certain ones

```python
ErrorHandler([Exception], [ZeroDivisionError])
```

In this case, exceptions like `ZeroDivisionError` will be skipped.

#### Respond to all descendants of a base exception

Let's imagine that the exception scheme looks like this:

```
BaseException
├── A
├── B
├── C
│ ├── C1
│ ├── C2
│ ├── C3
│ │ ├── C3_1
│ │ ├── C3_2
```

All BaseException heirs

```python
ErrorHandler([BaseException], [])
```

All C heirs: C1, C2, C3, C3_1, C3_2

```python
ErrorHandler([C], [])
```

All BaseException descendants except B

```python
ErrorHandler([BaseException], [B])
```

All BaseException heirs except C, But including C1, С2, C3, C3_1, C3_2

```python
ErrorHandler([BaseException], [C])
```
