from ..core.help import plugin_usage_formatter_with_default_start_indent
from ..core.plugin import get_all_plugins_by_type


def list_plugins() -> str:
    """
    Creates a string listing the plugins registered with wai-annotations,
    including details on their usage.
    """
    # Header
    result = "PLUGINS:\n"

    for type_string, plugins in get_all_plugins_by_type().items():
        result += f"  {type_string.upper()}:\n"
        for name, plugin in plugins.items():
            result += f"    {name.upper()}:\n"
            result += f"      {plugin.description()}\n\n"
            result += f"{plugin.format_usage(name, 6)}\n"

        # Additional separation between categories of plugins
        result += "\n"

    return result
