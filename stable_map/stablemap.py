from typing import Callable, Generic, Iterable, Sequence, TypeVar

from stable_map.context import ErrorContext, T
from stable_map.handler import ErrorHandler

S = TypeVar('S')


class StableMap(Generic[T, S]):
    __default: S | Callable[[ErrorContext[T, Exception]], S] | None
    __function: Callable[[T], S]
    __handlers: Sequence[ErrorHandler[T, Exception]]
    __sequence: Iterable[T]
