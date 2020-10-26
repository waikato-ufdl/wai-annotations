from typing import Type

from .._StageSpecifier import StageSpecifier
from .._ProcessorStageSpecifier import ProcessorStageSpecifier
from .._SinkStageSpecifier import SinkStageSpecifier
from .._SourceStageSpecifier import SourceStageSpecifier
from ._specifier_type import specifier_type


def specifier_type_string(specifier: Type[StageSpecifier]) -> str:
    """
    Returns a string describing the type of stage the given specifier specifies.

    :param specifier:   The stage specifier.
    :return:            A short name for the type of stage specified.
    """
    # Get the base type of the specifier
    specifier = specifier_type(specifier)

    if specifier is ProcessorStageSpecifier:
        return "processor stage"
    elif specifier is SinkStageSpecifier:
        return "sink stage"
    elif specifier is SourceStageSpecifier:
        return "source stage"
    else:
        raise Exception(f"Unknown specifier base type: {specifier}")
