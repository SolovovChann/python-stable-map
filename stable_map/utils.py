from typing import Callable, Iterable, Sequence

from stable_map.context import T
from stable_map.handler import ErrorHandler
from stable_map.stablemap import StableMap


def mutate(
    function: Callable[[T], None],
    sequence: Iterable[T],
    handlers: Sequence[ErrorHandler[T, Exception]],
) -> None:
    """
    Use this function if the function passed to `StableMap`
    mutates the original sequence and does not return anything
    """
    stable_map = StableMap(function, sequence, handlers)

    for _ in stable_map:
        pass
