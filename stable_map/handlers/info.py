import logging
import sys
from dataclasses import asdict
from typing import IO, Any, Callable, Sequence, TypeAlias

from stable_map.context import ErrorContext, ExceptionType, T
from stable_map.handler import ErrorHandler


class LoggingHandler(ErrorHandler[Any, Exception]):
    level: int
    message_format: str
    with_traceback: bool

    __logger: logging.Logger

    def __init__(
        self,
        logger: logging.Logger | str | None = None,
        message_format: str = "{index} element failed. Value={element}",
        level: int = logging.ERROR,
        with_traceback: bool = False,
        exceptions: Sequence[type[Exception]] = [Exception],
        ignore: Sequence[type[Exception]] = [],
    ) -> None:
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        super().__init__(exceptions, ignore)
        self.__logger = logger
        self.level = level
        self.message_format = message_format
        self.with_traceback = with_traceback

    def handle(self, context: ErrorContext[Any, Exception]) -> None:
        message = self._format_log_message(context)
        exception_info = context.exception if self.with_traceback else None

        self.__logger.log(self.level, message, exc_info=exception_info)

    def _format_log_message(self, context: ErrorContext[Any, Exception]) -> str:
        context_as_dict = asdict(context)
        msg_context = {key: repr(value) for key, value in context_as_dict.items()}

        return self.message_format.format(**msg_context)


ENCODER: TypeAlias = Callable[[ErrorContext[T, ExceptionType]], bytes | str]


def _encode_context(context: ErrorContext) -> str | bytes:
    return str(context.element)


class BufferWriter(ErrorHandler[T, ExceptionType]):
    __buffer: IO
    __encoding_callback: ENCODER[T, ExceptionType]

    def __init__(
        self,
        buffer: IO = sys.stderr,
        encoding_callback: ENCODER[T, ExceptionType] = _encode_context,
        exceptions: Sequence[type[ExceptionType]] = [Exception],
        ignore: Sequence[type[ExceptionType]] = [],
    ) -> None:
        super().__init__(exceptions, ignore)
        self.__buffer = buffer
        self.__encoding_callback = encoding_callback

    def handle(self, context: ErrorContext[T, ExceptionType]) -> None:
        assert self.__buffer.writable(), "Buffer is not writable"
        self.__buffer.write(self.__encoding_callback(context))
