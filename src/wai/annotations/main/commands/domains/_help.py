"""
Provides the help information for the 'domains' sub-command.
"""
from ._DomainsOptions import DomainsOptions


def domains_help() -> str:
    """
    Gets the help text for the 'domains' sub-command.
    """
    return DomainsOptions.get_configured_parser(prog="wai-annotations domains").format_help()
