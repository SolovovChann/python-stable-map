import logging

from stable_map.context import ErrorContext
from stable_map.handlers.info import LoggingHandler

from .test_error_handler import ErrorHandlerTest


class LoggingHandlerTest(ErrorHandlerTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.exceptions = [Exception, ZeroDivisionError, TypeError]
        cls.ignore = [IndentationError]
        cls.handler = LoggingHandler(
            exceptions=cls.exceptions,
            ignore=cls.ignore,
        )

    def test_handle(self) -> None:
        exception = ZeroDivisionError('expected exception')
        context = ErrorContext(42, 0, exception)

        with self.assertLogs(None, logging.ERROR):
            self.handler.handle(context)
