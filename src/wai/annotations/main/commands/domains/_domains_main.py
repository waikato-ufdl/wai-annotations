"""
Module containing the main entry point function for getting information about
domains registered with wai.annotations.
"""
from typing import Type

from wai.common.cli import OptionsList

from ....core.domain import DomainSpecifier
from ....core.plugin import get_all_domains
from ...logging import get_app_logger
from ._help import domains_help
from ._DomainsOptions import DomainsOptions


def domains_main(options: OptionsList):
    """
    Main method which handles the 'domains' sub-command. Prints the domains
    registered with wai.annotations.

    :param options:
                The options to the sub-command.
    """
    # Parse the options
    try:
        domains_options = DomainsOptions(options)
    except ValueError:
        get_app_logger().exception("Couldn't parse options to 'domains' command")
        print(domains_help())
        raise

    print(get_domains_formatted(domains_options))


def get_domains_formatted(options: DomainsOptions) -> str:
    """
    Gets a formatted string containing information about the domains
    registered with wai.annotations, the format of which is specified by
    the provided options.

    :param options:
                The formatting options.
    :return:
                The formatted domain information.
    """
    # If the help option is selected, print the usage and quit
    if options.HELP:
        print(domains_help())
        exit()

    # Get the domains registered with wai.annotations
    domains = list(get_all_domains())
    domains.sort(key=lambda domain: domain.name())

    # Filter to the specified domains
    if len(options.ONLY) > 0:
        domains = list(
            domain
            for domain in domains
            if domain.name() in options.ONLY
        )

    # Determine the formatting type
    cli_formatting = options.FORMATTING == "cli"

    # Header
    result = (
        "DOMAINS:\n"
        if cli_formatting else
        "# Domains\n"
    )

    # Get the formatting function for the selected style
    formatter =(
        format_domain_cli
        if cli_formatting else
        format_domain_markdown
    )

    # Format each domain
    for domain in domains:
        result += formatter(domain, options)

    return result


def format_domain_cli(
        domain: Type[DomainSpecifier],
        options: DomainsOptions
) -> str:
    """
    Formats a domain for the command-line.

    :param domain:
                The domain to format.
    :param options:
                The formatting options.
    :return:
                The formatted string.
    """
    # Add the domain's name
    result = f"  {domain.name()}\n"

    # Add the description if selected
    if options.DESCRIPTIONS:
        result += f"    {domain.description()}\n"

    return result


def format_domain_markdown(
        domain: Type[DomainSpecifier],
        options: DomainsOptions
) -> str:
    """
    Formats a domain in the markdown style.

    :param domain:
                The domain to format.
    :param options:
                The formatting options.
    :return:
                The formatted string.
    """
    # Format the domain's name
    result = f"## {domain.name()}\n"

    # Add the description of selected
    if options.DESCRIPTIONS:
        result += f"{domain.description()}\n\n"

    return result
