"""
Package for error types relating to core functionality.
"""
from ._BadDomain import BadDomain
from ._ConversionChainHasNoReader import ConversionChainHasNoReader
from ._ConversionChainHasNoWriter import ConversionChainHasNoWriter
from ._InputStageNotFirst import InputStageNotFirst
from ._StageAfterOutput import StageAfterOutput
from ._TooManyFormats import TooManyFormats
