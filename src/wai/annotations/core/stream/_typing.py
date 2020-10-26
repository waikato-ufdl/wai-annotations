from typing import TypeVar, Callable

# A generic type of element in a stream
ElementType = TypeVar("ElementType")

# The type of the function that continues the pipeline
ThenFunction = Callable[[ElementType], None]

# The type of the function that ends a stage of the pipeline
DoneFunction = Callable[[], None]
