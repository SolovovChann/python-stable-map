import abc
from typing import Generic

from stable_map.context import ExceptionType, T


class ErrorHandler(abc.ABC, Generic[T, ExceptionType]):
    ...
