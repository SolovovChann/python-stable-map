import abc
from typing import Generic, Sequence

from stable_map.context import ErrorContext, ExceptionType, T


class ErrorHandler(abc.ABC, Generic[T, ExceptionType]):
    """Handles the exceptions that occurred inside the `StableMap`"""

    __exceptions: Sequence[type[ExceptionType]]
    __ignore: Sequence[type[ExceptionType]]

    def __init__(
        self,
        exceptions: Sequence[type[ExceptionType]],
        ignore: Sequence[type[ExceptionType]] = [],
    ) -> None:
        """
        Note: the `exceptions` types is `covariant`
        and `ignore` types is `invariant`
        """
        self.__exceptions = exceptions
        self.__ignore = ignore

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
