from io import StringIO
from typing import Any, Callable
from unittest.mock import Mock

from stable_map.handler import ErrorContext
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

    def test_handle(self) -> None:
        context = ErrorContext(0, "test_element", Exception())

        self.encoding_callback.return_value = "encoded_context"
        self.handler.handle(context)
        self.assertEqual(self.buffer.getvalue(), "encoded_context")

    def test_handle_not_writable_buffer(self) -> None:
        self.buffer.writable = Mock(return_value=False)
        context = ErrorContext(0, "test_element", Exception())

        with self.assertRaises(AssertionError):
            self.handler.handle(context)
