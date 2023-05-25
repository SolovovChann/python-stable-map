from typing import Any

from stable_map.context import ErrorContext
from stable_map.handler import ErrorHandler


class RaiseExceptionHandler(ErrorHandler[Any, Exception]):
    """
    Add this handler to the `StableMap` to stop it's processing
    if any exception occurred.
    """

    def handle(self, context: ErrorContext[Any, Exception]) -> None:
        raise context.exception
