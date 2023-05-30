import logging
from dataclasses import asdict
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
        self.__logger.exception(
            message,
            exc_info=context.exception
        )

    def __format_log_message(self) -> str:
        context_as_dict = asdict(self.__context)
        context = {
            key: repr(value)
            for key, value in context_as_dict.items()
        }

        return self.message_format.format(**context)
