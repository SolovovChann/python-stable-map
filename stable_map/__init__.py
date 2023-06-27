"""
A tool similar to the built-in python map,
but reacting to exceptions that occur
"""

from .context import ErrorContext
from .handler import ErrorHandler
from .stablemap import StableMap
from .utils import mutate

__all__ = 'StableMap', 'ErrorHandler', 'ErrorContext', 'mutate'
__version__ = '1.0.0'
