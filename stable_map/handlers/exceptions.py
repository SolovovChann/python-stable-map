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
