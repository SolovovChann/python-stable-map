import logging
from typing import Any, Sequence

from stable_map.context import ErrorContext
from stable_map.handler import ErrorHandler


class LoggingHandler(ErrorHandler[Any, Exception]):
    message_format: str

    __context: ErrorContext[Any, Exception]
    __logger: logging.Logger

    def __init__(
        self,
        logger: logging.Logger | None = None,
        message_format: str = (
            '{exception} occurred while processing {index} element'
        ),
        exceptions: Sequence[type[Exception]] = [Exception],
        ignore: Sequence[type[Exception]] = [],
    ) -> None:
        if logger is None:
            logger = logging.getLogger(__name__)

        super().__init__(exceptions, ignore)
        self.__logger = logger
        self.message_format = message_format

    def handle(self, context: ErrorContext[Any, Exception]) -> None:
        self.__context = context
        message = self.__format_log_message()
        element_repr = self.__repr_element()

        self.__logger.debug(element_repr)
        self.__logger.exception(message, exc_info=context.exception)

    def __format_log_message(self) -> str:
        return (
            f'Exception occurred at {self.__context.index} '
            'element of sequence'
        )

    def __repr_element(self) -> str:
        return repr(self.__context.element)
