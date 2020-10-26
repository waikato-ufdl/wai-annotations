"""
Package for base stream-processing classes.
"""
from ._Pipeline import Pipeline
from ._StreamProcessor import StreamProcessor, InputElementType, OutputElementType
from ._StreamSink import StreamSink
from ._StreamSource import StreamSource
from ._typing import ThenFunction, DoneFunction, ElementType
