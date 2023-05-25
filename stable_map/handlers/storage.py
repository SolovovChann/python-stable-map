import pickle
from pathlib import Path
from typing import Any, Callable

from stable_map.context import ErrorContext
from stable_map.handler import ErrorHandler


class PickleHandler(ErrorHandler[Any, Exception]):
    __context: ErrorContext[Any, Exception]
    __dest: Path
    __file_name: str | Path | Callable[
        [ErrorContext[Any, Exception]], str | Path
    ]
