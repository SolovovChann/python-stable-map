import pickle
from pathlib import Path
from typing import Any, Callable, Sequence

from stable_map.context import ErrorContext
from stable_map.handler import ErrorHandler


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
