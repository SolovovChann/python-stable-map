from stable_map.context import ErrorContext
from stable_map.handlers.exceptions import RaiseExceptionHandler

from .test_error_handler import ErrorHandlerTest
from .test_error_handler import ExceptionStructure as Exc


class RaiseExceptionHandlerTest(ErrorHandlerTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.exceptions = [Exc.FirstLevel, Exc.SecondLevel, Exc.SubThird]
        cls.ignore = [Exc.ThirdLevel, Exc.Base]
        cls.handler = RaiseExceptionHandler(
            exceptions=cls.exceptions,
            ignore=cls.ignore,
        )

    def test_handle(self) -> None:
        exception = ZeroDivisionError("expected exception")
        context = ErrorContext(42, "expected exception", exception)

        with self.assertRaises(ZeroDivisionError):
            self.handler.handle(context)
