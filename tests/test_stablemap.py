import unittest
from typing import Any

from stable_map.context import ErrorContext
from stable_map.handler import ErrorHandler


class ErrorHandlerStub(ErrorHandler[Any, Exception]):
    def handle(self, context: ErrorContext[Any, Exception]) -> None:
        pass


def divide_100_to(divider: float) -> float:
    return 100 // divider


class StableMapTest(unittest.TestCase):
    ...
