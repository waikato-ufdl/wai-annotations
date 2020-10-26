from .._StreamSink import StreamSink
from .._typing import ElementType, ThenFunction
from ._RequiresNoFinalisation import RequiresNoFinalisation


class FunctionStreamSink(
    RequiresNoFinalisation,
    StreamSink[ElementType]
):
    """
    A stream-sink that simply calls a function for each element.
    """
    def __init__(self, function: ThenFunction[ElementType]):
        # The function to call
        self._function: ThenFunction[ElementType] = function

    def consume_element(self, element: ElementType):
        # Call the function with the element as the argument
        self._function(element)
