from typing import Generic, TypeVar

from stable_map.context import T

S = TypeVar('S')


class StableMap(Generic[T, S]):
    ...
