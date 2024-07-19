import abc
import pickle
import re
from pathlib import Path
from typing import Any, ByteString, Callable, Sequence, TypeAlias

from stable_map.context import ErrorContext, ExceptionType, T
from stable_map.handler import ErrorHandler


FILENAME_HANDLER: TypeAlias = Callable[[ErrorContext[T, ExceptionType]], str]
FILENAME_TYPE: TypeAlias = str | FILENAME_HANDLER


def pascal_to_snake(string: str, divider: str = "_") -> str:
    """Convert string in pascal case to snake case"""
    string = re.sub(r"(.)([A-Z][a-z]+)", r"\1" + divider + r"\2", string)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1" + divider + r"\2", string)


def make_file_name(extension: str) -> FILENAME_HANDLER:
    def wrapper(context: ErrorContext[Any, Exception]) -> str:
        element_type = context.element.__class__.__name__
        element_type = pascal_to_snake(element_type).lower()

        return f"{element_type}_{context.index}.{extension}".strip()

    return wrapper


class Storage(ErrorHandler[T, ExceptionType]):
    """Create save directory and store failed object in it"""

    __filename: FILENAME_TYPE
    __mode: int
    __save_dir: Path

    def __init__(
        self,
        save_dir: Path | str = Path("."),
        mode: int = 751,
        file_name: FILENAME_TYPE = make_file_name("undefined"),
        exceptions: Sequence[type[ExceptionType]] = [Exception],
        ignore: Sequence[type[ExceptionType]] = [],
    ) -> None:
        if not isinstance(save_dir, Path):
            save_dir = Path(save_dir)

        super().__init__(exceptions, ignore)
        self.__filename = file_name
        self.__mode = mode
        self.__save_dir = save_dir

    def handle(self, context: ErrorContext[T, ExceptionType]) -> None:
        self._prepare_make_dir()

        file_path = self._make_file_path(context)
        content = self._encode_content(context.element)
        file_path.write_bytes(content)

    @abc.abstractmethod
    def _encode_content(self, element: T) -> ByteString: ...

    def _prepare_make_dir(self) -> None:
        if not self.__save_dir.exists():
            self.__save_dir.mkdir(self.__mode, parents=True)
        else:
            self.__save_dir.chmod(self.__mode)

    def _make_file_path(self, context: ErrorContext[T, ExceptionType]) -> Path:
        return self.__save_dir / self._make_filename(context)

    def _make_filename(self, context: ErrorContext[T, ExceptionType]) -> str:
        if callable(self.__filename):
            return self.__filename(context)

        return self.__filename


def _get_default_file_name(context: ErrorContext[Any, Exception]) -> str:
    element_type = type(context.element).__name__.lower()
    index = context.index

    return f'{element_type}_{index}.pickle'


class PickleDumpHandler(ErrorHandler[Any, Exception]):
    __context: ErrorContext[Any, Exception]
    __dest: Path
    __file_name: str | Path | Callable[
        [ErrorContext[Any, Exception]], str | Path
    ]

    def __init__(
        self,
        dest: Path | str,
        exceptions: Sequence[type[Exception]] = [Exception],
        ignore: Sequence[type[Exception]] = [],
        file_name: str | Path | Callable[
            [ErrorContext[Any, Exception]], str | Path
        ] = _get_default_file_name,
    ) -> None:
        if isinstance(dest, str):
            dest = Path(dest)

        super().__init__(exceptions, ignore)
        self.__dest = dest
        self.__file_name = file_name

    def handle(self, context: ErrorContext[Any, Exception]) -> None:
        self.__context = context
        output_file = self.__dest / self.__eval_file_name()
        data = self.__dump_data()

        output_file.write_bytes(data)

    def __eval_file_name(self) -> Path:
        if callable(self.__file_name):
            file_name = self.__file_name(self.__context)
        else:
            file_name = self.__file_name

        if isinstance(file_name, str):
            file_name = Path(file_name)

        return file_name

    def __dump_data(self) -> Any:
        element = self.__context.element
        data = pickle.dumps(element)

        return data
