import unittest
from typing import Any
from unittest import mock

from stable_map.context import ErrorContext
from stable_map.handler import ErrorHandler
from stable_map.stablemap import StableMap


class ErrorHandlerStub(ErrorHandler[Any, Exception]):
    def handle(self, context: ErrorContext[Any, Exception]) -> None:
        pass


def divide_100_to(divider: float) -> float:
    return 100 // divider


class StableMapTest(unittest.TestCase):
    def test_iteration(self) -> None:
        sequence = [3, 4, 1, 2, 0, 5, 8]
        reference = [33, 25, 100, 50, 20, 12]

        handler = ErrorHandlerStub([Exception], [])
        handler.handle = mock.MagicMock()

        stable_map = StableMap(divide_100_to, sequence, [handler])

        for value, ref in zip(stable_map, reference):
            self.assertEqual(value, ref)
