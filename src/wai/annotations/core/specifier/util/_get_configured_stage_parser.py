from typing import Type

from .._StageSpecifier import StageSpecifier


def get_configured_stage_parser(specifier: Type[StageSpecifier], **kwargs):
    """
    Gets a parser which is configured to parse the options
    for all components of the given stage specifier.

    :param specifier:   The specifier to create the parser for.
    :param kwargs:      Any additional arguments to the parser.
    :return:            The configured parser for the stage.
    """
    # Get the components of the stage
    component_types = specifier.components()

    # Configure a parser on the first component
    parser = component_types[0].get_configured_parser(**kwargs)

    # Update the parser with the remaining components
    for component in component_types[1:]:
        component.configure_parser(parser)

    return parser
