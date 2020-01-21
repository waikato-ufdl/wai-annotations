from typing import Callable, Iterable

from .._InlineStreamProcessor import InlineStreamProcessor, StreamElementType


class StreamLogger(InlineStreamProcessor[StreamElementType]):
    """
    Stream processor that logs a message for each item in the stream.
    """
    def __init__(self,
                 logging_method: Callable[[str], None],
                 message_formatter: Callable[[StreamElementType], str]):
        # Logger method to use to log the message (e.g. logger.info)
        self._logging_method: Callable[[str], None] = logging_method

        # Function to convert a stream element into a log message (e.g. lambda e: f"Processing element: {e.name}")
        self._message_formatter: Callable[[StreamElementType], str] = message_formatter

    def _process_element(self, element: StreamElementType) -> Iterable[StreamElementType]:
        # Log the message
        self._logging_method(self._message_formatter(element))

        return element,
