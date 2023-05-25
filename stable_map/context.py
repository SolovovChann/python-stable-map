from dataclasses import dataclass
from typing import Generic, TypeVar

ExceptionType = TypeVar('ExceptionType', bound=Exception)
T = TypeVar('T')


@dataclass
class ErrorContext(Generic[T, ExceptionType]):
    index: int
    element: T
    exception: ExceptionType
