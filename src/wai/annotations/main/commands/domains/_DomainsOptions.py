from argparse import ArgumentParser

from wai.common.cli import CLIInstantiable
from wai.common.cli.options import FlagOption, TypedOption

from ....core.plugin import get_all_domains


class DomainsOptions(CLIInstantiable):
    """
    The options for the 'domains' command.
    """
    ONLY = TypedOption(
        "-o", "--only",
        type=str,
        nargs="+",
        choices=tuple(domain.name() for domain in get_all_domains()),
        help="restrict the set of domains to only those specified",
        metavar="DOMAIN"
    )

    DESCRIPTIONS = FlagOption(
        "-d", "--no-descriptions",
        invert=True,
        help="whether to suppress the descriptions of the plugins"
    )

    FORMATTING = TypedOption(
        "-f", "--formatting",
        type=str,
        choices=("cli", "markdown"),
        default="cli",
        help="the formatting style to print the domains in"
    )

    # Override the default help option
    HELP = FlagOption(
        "-h", "--help",
        help="prints this help message and exits"
    )

    @classmethod
    def get_configured_parser(cls, *, add_help=False, **kwargs) -> ArgumentParser:
        return super().get_configured_parser(add_help=add_help, **kwargs)
