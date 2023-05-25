from typing import Any

from stable_map.context import ErrorContext
from stable_map.handler import ErrorHandler


class RaiseExceptionHandler(ErrorHandler[Any, Exception]):
    def handle(self, context: ErrorContext[Any, Exception]) -> None:
        raise context.exception