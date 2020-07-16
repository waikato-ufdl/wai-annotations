from abc import ABC, abstractmethod
from argparse import Namespace
from typing import Any

from wai.common.cli import ArgumentParserConfigurer, OptionsList

from ..help import plugin_usage_formatter_with_default_start_indent


class PluginSpecifier(ArgumentParserConfigurer, ABC):
    """
    Base class for classes which specify the components of a plugin.
    """
    @classmethod
    @abstractmethod
    def type_string(cls) -> str:
        """
        Gets a string representation of the type of plugin this specifies.
        """
        pass

    @classmethod
    def instantiate_stage(cls, options: OptionsList) -> Any:
        """
        Creates an instance of the stage represented by this plugin
        using the given command-line options.

        :param options:     The command-line options.
        :return:            The stage.
        """
        # Parse the command-line arguments
        namespace = cls.get_configured_parser(add_help=False).parse_args(options)

        return cls.stage_instance_from_namespace(namespace)

    @classmethod
    @abstractmethod
    def stage_instance_from_namespace(cls, namespace: Namespace) -> Any:
        """
        Creates an instance of the processing stage represented by this plugin
        from the parsed namespace.

        :param namespace:   The namespace.
        :return:            The plugin stage.
        """
        pass

    @classmethod
    @abstractmethod
    def description(cls) -> str:
        """
        A short description of the functionality the plugin component provides.
        """
        pass

    @classmethod
    @abstractmethod
    def format_domain_description(cls) -> str:
        """
        Formats the domain information for the plugin.
        """
        pass

    @classmethod
    def format_usage(cls, name: str, indent: int = 0) -> str:
        """
        Gets the usage text for the plugin.

        :param name:        The name the plugin is registered under in the plugin system.
        :param indent:      The indentation level of the text.
        :return:            The usage text.
        """
        return (" " * indent) + cls.get_configured_parser(
            prog=name,
            add_help=False,
            formatter_class=plugin_usage_formatter_with_default_start_indent(indent)
        ).format_help()
