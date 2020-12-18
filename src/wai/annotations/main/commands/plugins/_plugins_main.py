from typing import Type, Dict

from wai.common.cli import OptionsList

from ....core.help import format_stage_usage
from ....core.plugin import get_all_plugins, get_plugin_domains
from ....core.specifier import *
from ....core.specifier.util import specifier_type_string
from ...logging import get_app_logger
from ._help import plugins_help
from ._PluginsOptions import PluginsOptions

# Lookup from the type option to the sub-class for filtering
plugin_types_lookup = {
    "source": SourceStageSpecifier,
    "processor": ProcessorStageSpecifier,
    "sink": SinkStageSpecifier
}


def plugins_main(options: OptionsList):
    """
    Main method which handles the 'plugins' sub-command. Prints the plugins
    registered with wai.annotations.

    :param options:
                The options to the sub-command.
    """
    # Parse the options
    try:
        plugins_options = PluginsOptions(options)
    except ValueError:
        get_app_logger().exception("Couldn't parse options to 'plugins' command")
        print(plugins_help())
        raise

    print(get_plugins_formatted(plugins_options))


def get_plugins_formatted(options: PluginsOptions) -> str:
    """
    Gets a formatted string containing information about the plugins
    registered with wai.annotations, formatted according to the
    provided options.

    :param options:
                The formatting options.
    :return:
                The formatted string.
    """
    # If the help option is selected, print the usage and quit
    if options.HELP:
        print(plugins_help())
        exit()

    # Get the plugins registered with wai.annotations
    plugins = get_all_plugins()

    # Filter to the specified plugins
    if len(options.ONLY) > 0:
        plugins = {
            name: plugins[name]
            for name in options.ONLY
            if name in plugins
        }

    # Filter to the specified types
    if len(options.ONLY_TYPES) > 0:
        # Use the lookup to translate strings into specifier sub-classes
        only_types = tuple(
            plugin_types_lookup[type]
            for type in options.ONLY_TYPES
        )

        # Filter the plugins to the specified sub-classes
        plugins = {
            name: specifier
            for name, specifier in plugins.items()
            if issubclass(specifier, only_types)
        }

    return (
        plugins_by_type(
            {
                type: {
                    name: specifier
                    for name, specifier in plugins.items()
                    if issubclass(specifier, type)
                }
                for type in (SourceStageSpecifier, ProcessorStageSpecifier, SinkStageSpecifier)
            },
            options
        )
        if options.GROUP_BY_TYPE else
        plugins_no_type(plugins, options)
    )


def plugins_by_type(
        plugins: Dict[Type[StageSpecifier], Dict[str, Type[StageSpecifier]]],
        options: PluginsOptions
) -> str:
    """
    Formats the plugins when the group-by-type option is selected.

    :param plugins:
                The plugins, grouped by type.
    :param options:
                The formatting options.
    :return:
                The formatted string.
    """
    # Check if we are doing CLI or Markdown formatting
    cli_formatting = options.FORMATTING == "cli"

    # Header
    result = (
        "PLUGINS:\n"
        if cli_formatting else
        "# Plugins\n"
    )

    # If all plugins are filtered out, display None
    if len(plugins) == 0:
        result += (
            "  NONE\n"
            if cli_formatting else
            "\nNone\n"
        )

    # Choose a formatter based on the option
    formatter = (
        format_plugin_cli
        if cli_formatting else
        format_plugin_markdown
    )

    for base_type, plugins_for_type in plugins.items():
        # Skip empty types
        if len(plugins_for_type) == 0:
            continue

        # Get the name of the type of plugin
        base_type_string = specifier_type_string(base_type)

        # Add aheading for the type
        result += (
            f"  {base_type_string.upper()}:\n"
            if cli_formatting else
            f"## {base_type_string.capitalize()}\n"
        )

        # Sort the plugins by name
        names_sorted = list(plugins_for_type.keys())
        names_sorted.sort()

        # Format each plugin
        for name in names_sorted:
            result += formatter(name, plugins_for_type[name], options, 6)

        # Additional separation between categories of plugins
        result += "\n"

    return result


def plugins_no_type(
        plugins: Dict[str, Type[StageSpecifier]],
        options: PluginsOptions
) -> str:
    """
    Formats the plugins when not grouped by type.

    :param plugins:
                The plugins to format.
    :param options:
                The formatting options.
    :return:
                The formatted plugins.
    """
    # See if we're doing CLI or Markdown formatting
    cli_formatting = options.FORMATTING == "cli"

    # Header
    result = (
        "PLUGINS:\n"
        if cli_formatting else
        "# Plugins\n"
    )

    # Choose a formatter based on the selected style
    formatter = (
        format_plugin_cli
        if cli_formatting else
        format_plugin_markdown
    )

    # Sort the plugins by name
    names_sorted = list(plugins.keys())
    names_sorted.sort()

    # Show 'none' if there are no matched plugins
    if len(names_sorted) == 0:
        result += (
            "  NONE\n"
            if cli_formatting else
            "\nNone\n"
        )

    # Format the plugins
    for name in names_sorted:
        result += formatter(name, plugins[name], options, 4)

    return result


def format_plugin_cli(
        plugin_name: str,
        plugin: Type[StageSpecifier],
        options: PluginsOptions,
        indent: int
):
    """
    Formats a plugin for the command-line.

    :param plugin_name:
                The name of the plugin.
    :param plugin:
                The plugin specifier.
    :param options:
                The formatting options.
    :param indent:
                The level of indentation.
    :return:
                The formatted plugin.
    """
    # Format the indentation string
    indentation = " " * indent

    # Add the name
    formatted = f"{indentation}{plugin_name.upper()}"

    # Add a : if there are any other descriptions of the plugin
    if options.DESCRIPTIONS or options.DOMAINS or options.OPTIONS:
        formatted += ":"
    formatted += "\n"

    # Add the description if not suppressed
    if options.DESCRIPTIONS:
        formatted += f"{indentation}  {plugin.description()}\n\n"

    # Add the domains if not suppressed
    if options.DOMAINS:
        domains = ", ".join(domain.name() for domain in get_plugin_domains(plugin))
        formatted += f"{indentation}  Domain(s): {domains}\n\n"

    # Add the options if not suppressed
    if options.OPTIONS:
        formatted += f"{format_stage_usage(plugin, plugin_name, indent + 2)}\n"

    return formatted


def format_plugin_markdown(
        plugin_name: str,
        plugin: Type[StageSpecifier],
        options: PluginsOptions,
        indent: int
):
    """
    Formats a plugin in Markdown style.

    :param plugin_name:
                The name of the plugin.
    :param plugin:
                The plugin specifier.
    :param options:
                The formatting options.
    :param indent:
                The level of indentation.
    :return:
                The formatted plugin.
    """
    # Format the indentation string
    indentation = "#" * (indent // 2)

    # Format the plugin name
    formatted = f"{indentation} {plugin_name.upper()}\n"

    # Add the description if not suppressed
    if options.DESCRIPTIONS:
        formatted += f"{plugin.description()}\n\n"

    # Add the domains if not suppressed
    if options.DOMAINS:
        domains = "\n".join(f"- **{domain.name()}**" for domain in get_plugin_domains(plugin))
        formatted += f"{indentation}# Domain(s):\n{domains}\n\n"

    # Add the options if not suppressed
    if options.OPTIONS:
        formatted += f"{indentation}# Options:\n```\n{format_stage_usage(plugin, plugin_name, 0)}```\n\n"

    return formatted
