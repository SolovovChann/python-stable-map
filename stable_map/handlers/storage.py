import pickle
from pathlib import Path
from typing import Any, Callable, Sequence

from stable_map.context import ErrorContext
from stable_map.handler import ErrorHandler


def __get_default_file_name(context: ErrorContext[Any, Exception]) -> str:
    exc_type = type(context.exception)
    index = context.index

    return f'{exc_type}_{index}'


class PickleHandler(ErrorHandler[Any, Exception]):
    __context: ErrorContext[Any, Exception]
    __dest: Path
    __file_name: str | Path | Callable[
        [ErrorContext[Any, Exception]], str | Path
    ]

    def __init__(
        self,
        exceptions: Sequence[type[Exception]],
        ignore: Sequence[type[Exception]],
        dest: Path,
        file_name: str | Path | Callable[
            [ErrorContext[Any, Exception]], str | Path
        ] = __get_default_file_name,
    ) -> None:
        super().__init__(exceptions, ignore)
        self.__dest = dest
        self.__file_name = file_name

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
