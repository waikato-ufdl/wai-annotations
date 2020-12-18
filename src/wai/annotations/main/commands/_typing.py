"""
Types related to sub-commands.
"""
from typing import Callable

from wai.common.cli import OptionsList

# The type of a sub-command main function
CommandMain = Callable[[OptionsList], None]
