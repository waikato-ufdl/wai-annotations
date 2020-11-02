"""
Package of errors that can occur while building a conversion pipeline.
"""
from ._BadDomain import BadDomain
from ._InputStageNotFirst import InputStageNotFirst
from ._StageAfterOutput import StageAfterOutput
from ._StageInvalidForDomains import StageInvalidForDomains
