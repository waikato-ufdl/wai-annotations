from typing import Callable, TypeVar

from ..stream import StreamProcessor, ThenFunction, DoneFunction
from ..stream.util import RequiresNoFinalisation

InputElementType = TypeVar("InputElementType")


class StreamLogger(
    RequiresNoFinalisation,
    StreamProcessor[InputElementType, InputElementType]
):
    """
    Stream processor that logs a message for each item in the stream,
    subject to a predicate.
    """
    def __init__(self,
                 logging_method: Callable[[str], None],
                 message_formatter: Callable[[InputElementType], str],
                 predicate: Callable[[InputElementType], bool] = lambda stream_element: True):
        # Logger method to use to log the message (e.g. logger.info)
        self._logging_method: Callable[[str], None] = logging_method

        # Function to convert a stream element into a log message (e.g. lambda e: f"Processing element: {e.name}")
        self._message_formatter: Callable[[InputElementType], str] = message_formatter

        # Predicate which decides which elements should be logged
        self._predicate = predicate

    def process_element(
            self,
            element: InputElementType,
            then: ThenFunction[InputElementType],
            done: DoneFunction
    ):
        # Log the message
        if self._predicate(element):
            self._logging_method(self._message_formatter(element))

        then(element)
