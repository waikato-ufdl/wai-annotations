from ...component import *
from .._StageSpecifier import StageSpecifier
from .._ProcessorStageSpecifier import ProcessorStageSpecifier
from .._SinkStageSpecifier import SinkStageSpecifier
from .._SourceStageSpecifier import SourceStageSpecifier


def validate_stage_specifier(specifier):
    """
    Ensures that a stage specifier has been properly configured.

    :param specifier:   The specifier to check.
    """

    if not issubclass(specifier, StageSpecifier):
        raise Exception("Not a stage specifier")

    components = specifier.components()

    # Make sure the components are a tuple
    if not isinstance(components, tuple):
        raise Exception("Components not specified as a tuple")

    # Make sure at least one component is specified
    if len(components) == 0:
        raise Exception("No components specified")

    if issubclass(specifier, SourceStageSpecifier):
        if not issubclass(components[0], SourceComponent):
            raise Exception("Source stage must begin with source component")
        if not all(issubclass(component, ProcessorComponent) for component in components[1:]):
            raise Exception("All subsequent components of a source stage must be processors")

    elif issubclass(specifier, ProcessorStageSpecifier):
        if not all(issubclass(component, ProcessorComponent) for component in components):
            raise Exception("Processor stage can only consist of processor components")

    elif issubclass(specifier, SinkStageSpecifier):
        if not all(issubclass(component, ProcessorComponent) for component in components[:-1]):
            raise Exception("All preceding components of a sink stage must be processors")
        if not issubclass(components[-1], SinkComponent):
            raise Exception("Sink stage must end with sink component")

    else:
        raise Exception("Unknown stage specifier type")
