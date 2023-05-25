import abc
from typing import Generic, Sequence

from stable_map.context import ExceptionType, T


class ErrorHandler(abc.ABC, Generic[T, ExceptionType]):
    __exceptions: Sequence[type[ExceptionType]]
    __ignore: Sequence[type[ExceptionType]]
