"""
Functionality for working with the available commands as a group.
"""
from typing import Dict, List

from .convert import convert_main
from .domains import domains_main
from .plugins import plugins_main
from ._typing import CommandMain

# The mapping from command names to main functions for those commands
__commands: Dict[str, CommandMain] = {
    "convert": convert_main,
    "plugins": plugins_main,
    "domains": domains_main
}


def get_command_main(command: str) -> CommandMain:
    """
    Gets the main function of the given command.

    :param command:
                The command.
    :return:
                The main function to call to perform the command.
    """
    if command not in __commands:
        raise Exception(f"Unknown command '{command}'")

    return __commands[command]


def list_commands() -> List[str]:
    """
    Gets the list of available commands.

    :return:
                The list of commands.
    """
    return list(__commands.keys())
