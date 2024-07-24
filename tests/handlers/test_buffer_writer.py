from io import StringIO
from typing import Any, Callable
from unittest.mock import Mock

from stable_map.handlers.info import ENCODER, BufferWriter

from .test_error_handler import ErrorHandlerTest


class BufferWriterTest(ErrorHandlerTest):
    buffer: StringIO
    encoding_callback: Callable[[Any], str]

    @classmethod
    def setUpClass(cls):
        cls.buffer = StringIO()
        cls.encoding_callback = Mock(spec=ENCODER)
        cls.handler = BufferWriter(cls.buffer, cls.encoding_callback)
        cls.exceptions = [Exception]
        cls.ignore = []
