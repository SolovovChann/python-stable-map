import abc
from typing import Generic, Sequence

from stable_map.context import ErrorContext, ExceptionType, T


class ErrorHandler(abc.ABC, Generic[T, ExceptionType]):
    __exceptions: Sequence[type[ExceptionType]]
    __ignore: Sequence[type[ExceptionType]]

    @abc.abstractmethod
    def handle(self, context: ErrorContext[T, ExceptionType]) -> None:
        ...

    def is_react_to(self, exception: Exception) -> bool:
        is_ignores = type(exception) in self.__ignore
        is_react = any(
            isinstance(exception, exc_type)
            for exc_type in self.__exceptions
        )

        return is_react and not is_ignores
