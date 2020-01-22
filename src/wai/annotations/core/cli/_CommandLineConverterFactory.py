from abc import ABC
from typing import TypeVar

from .._Converter import Converter
from ._CommandLineFactory import CommandLineFactory

# Type variable for the related converter class that this factory produces
RelatedConverterClass = TypeVar("RelatedConverterClass", bound=Converter)


class CommandLineConverterFactory(CommandLineFactory[RelatedConverterClass], ABC):
    """
    Base class for command-line factories that produce converters.
    """
    pass
