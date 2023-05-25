from typing import Callable, Generic, Iterable, Sequence, TypeVar

from stable_map.context import ErrorContext, T
from stable_map.handler import ErrorHandler

S = TypeVar('S')


class StableMap(Generic[T, S]):
    __default: S | Callable[[ErrorContext[T, Exception]], S] | None
    __function: Callable[[T], S]
    __handlers: Sequence[ErrorHandler[T, Exception]]
    __sequence: Iterable[T]
    __context: ErrorContext[T, Exception]

    def __init__(
        self,
        function: Callable[[T], S],
        sequence: Iterable[T],
        handlers: Sequence[ErrorHandler[T, Exception]],
        default: S | Callable[[ErrorContext[T, Exception]], S] | None = None,
    ) -> None:
        self.__default = default
        self.__function = function
        self.__handlers = handlers
        self.__sequence = sequence
