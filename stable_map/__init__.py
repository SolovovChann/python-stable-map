"""
A tool similar to the built-in python map,
but reacting to exceptions that occur
"""

from .context import ErrorContext
from .handler import ErrorHandler
from .stablemap import StableMap

__all__ = 'StableMap', 'ErrorHandler', 'ErrorContext'
__version__ = '0.1.0'
