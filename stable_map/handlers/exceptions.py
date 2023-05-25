import logging
from typing import Any, Sequence

from stable_map.context import ErrorContext
from stable_map.handler import ErrorHandler


class RaiseExceptionHandler(ErrorHandler[Any, Exception]):
    """
    Add this handler to the `StableMap` to stop it's processing
    if any exception occurred.
    """

    def handle(self, context: ErrorContext[Any, Exception]) -> None:
        raise context.exception


class LoggingHandler(ErrorHandler[Any, Exception]):
    logger: logging.Logger

    __context: ErrorContext[Any, Exception]

    def __init__(
        self,
        exceptions: Sequence[type[Exception]],
        ignore: Sequence[type[Exception]],
        logger: logging.Logger | None = None,
    ) -> None:
        if logger is None:
            logger = logging.getLogger(__name__)

        super().__init__(exceptions, ignore)
        self.logger = logger

    def handle(self, context: ErrorContext[Any, Exception]) -> None:
        self.__context = context
        message = self.__format_log_message()
        element_repr = self.__repr_element()

        self.logger.debug(element_repr)
        self.logger.exception(message, exc_info=context.exception)

    def __format_log_message(self) -> str:
        return (
            f'Exception occurred at {self.__context.index} '
            'element of sequence'
        )

    def __repr_element(self) -> str:
        return repr(self.__context.element)
