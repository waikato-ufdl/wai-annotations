from typing import Type

from .._StageSpecifier import StageSpecifier
from .._ProcessorStageSpecifier import ProcessorStageSpecifier
from .._SinkStageSpecifier import SinkStageSpecifier
from .._SourceStageSpecifier import SourceStageSpecifier


def specifier_type(specifier: Type[StageSpecifier]) -> Type[StageSpecifier]:
    """
    Returns a base type type of stage the given specifier specifies.

    :param specifier:   The stage specifier.
    :return:            The specifier base-type
    """
    if issubclass(specifier, ProcessorStageSpecifier):
        return ProcessorStageSpecifier
    elif issubclass(specifier, SinkStageSpecifier):
        return SinkStageSpecifier
    elif issubclass(specifier, SourceStageSpecifier):
        return SourceStageSpecifier
    else:
        raise Exception(f"Unknown specifier type: {specifier}")
