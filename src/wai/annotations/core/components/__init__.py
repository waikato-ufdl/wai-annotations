"""
Package for base classes for the four component types:

Readers, input converters, output converters and writers.
"""
from ._ExternalFormatConverter import ExternalFormatConverter
from ._InternalFormatConverter import InternalFormatConverter
from ._JSONWriter import JSONWriter
from ._Reader import Reader
from ._SeparateImageWriter import SeparateImageWriter
from ._Writer import Writer
