from typing import Callable, Generator, Generic, Iterable, Sequence, TypeVar

from stable_map.context import ErrorContext, T
from stable_map.handler import ErrorHandler


S = TypeVar("S")


class StableMap(Generic[T, S]):
    """
    Same as the built-in `map` but reacts and handles
    the occurred exceptions rather than breaking the loop.
    """

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

    def __iter__(self) -> Generator[S, None, None]:
        for index, element in enumerate(self.__sequence):
            try:
                yield self.__function(element)
            except Exception as exc:
                self.__context = ErrorContext(index, element, exc)
                self.__handle_exception()

                if self.__default is not None:
                    yield self.__eval_default_value()

    def __handle_exception(self) -> None:
        for handler in self.__get_specific_exc_handlers():
            handler.handle(self.__context)

    def __get_specific_exc_handlers(self) -> list[ErrorHandler[T, Exception]]:
        exception = self.__context.exception

        return [
            handler
            for handler in self.__handlers
            if handler.is_react_to(exception)
        ]

    def __eval_default_value(self) -> S:
        assert self.__default is not None

        if callable(self.__default):
            return self.__default(self.__context)

        return self.__default
