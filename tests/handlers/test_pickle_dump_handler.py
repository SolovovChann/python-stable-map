from pathlib import Path
from tempfile import mkdtemp
from typing import Any, Callable

from stable_map.context import ErrorContext
from stable_map.handlers.storage import PickleDumpHandler

from .test_error_handler import ErrorHandlerTest


def get_file_name(context: ErrorContext[Any, Exception]) -> str:
    return f'{context.index}.pickle'


class PickleDumpHandlerTest(ErrorHandlerTest):
    file_name_func: Callable[[ErrorContext[Any, Exception]], str]
    storage_dir: Path

    @classmethod
    def setUpClass(cls) -> None:
        cls.storage_dir = Path(mkdtemp())
        cls.exceptions = [Exception, ZeroDivisionError, TypeError]
        cls.ignore = [IndentationError]
        cls.handler = PickleDumpHandler(
            cls.storage_dir,
            file_name=get_file_name,
            exceptions=cls.exceptions,
            ignore=cls.ignore,
        )

    def test_handle(self) -> None:
        exception = ZeroDivisionError('expected exception')
        context = ErrorContext(42, 'expected exception', exception)
        file_name = get_file_name(context)
        storage_file = self.storage_dir / file_name
        self.handler.handle(context)

        self.assertTrue(storage_file.exists())
