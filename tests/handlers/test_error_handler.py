import unittest
from typing import Any

from stable_map.handler import ErrorHandler


class ExceptionStructure:
    """Test ErrorHandler exceptions and ignore statements"""

    class Base(Exception):
        ...

    class FirstLevel(Base):
        ...

    class SubFirst(FirstLevel):
        ...

    class SecondLevel(FirstLevel):
        ...

    class SubSecond(SecondLevel):
        ...

    class ThirdLevel(SecondLevel):
        ...

    class SubThird(ThirdLevel):
        ...

    all = (
        Base,
        FirstLevel,
        SubFirst,
        SecondLevel,
        SubSecond,
        ThirdLevel,
        SubThird,
    )


class ErrorHandlerTest(unittest.TestCase):
    handler: ErrorHandler[Any, Exception]
    exceptions: list[type[Exception]]
    ignore: list[type[Exception]]

    @classmethod
    def setUpClass(cls) -> None:
        raise unittest.SkipTest('Interface is not implemented')

    def test_is_react_to(self) -> None:
        for exc_type in self.exceptions:
            exc = exc_type()
            self.assertTrue(self.handler.is_react_to(exc))

    def test_is_react_to_ignore(self) -> None:
        for exc_type in self.ignore:
            exc = exc_type()
            self.assertFalse(self.handler.is_react_to(exc))

    def test_handle(self) -> None:
        raise NotImplementedError
