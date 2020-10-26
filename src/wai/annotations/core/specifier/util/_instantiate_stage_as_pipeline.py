from typing import Type

from wai.common.cli import OptionsList

from ...component import *
from ...stream import Pipeline
from .._StageSpecifier import StageSpecifier
from ._get_configured_stage_parser import get_configured_stage_parser


def instantiate_stage_as_pipeline(specifier: Type[StageSpecifier], options: OptionsList) -> Pipeline:
    """
    Creates an instance of the stage represented by this plugin
    as a pipeline, using the given command-line options.

    :param specifier:   The stage specifier to instantiate.
    :param options:     The command-line options.
    :return:            The stage as a pipeline.
    """
    # Instantiate all of the stage's components from the options
    namespace = get_configured_stage_parser(specifier).parse_args(options)
    components = tuple(component_type(namespace) for component_type in specifier.components())

    source = None
    sink = None

    if isinstance(components[0], SourceComponent):
        source = components[0]
        components = components[1:]

    if isinstance(components[-1], SinkComponent):
        sink = components[-1]
        components = components[:-1]

    return Pipeline(
        source=source,
        processors=components,
        sink=sink
    )
