import os
from typing import Optional

from ._get_default_macro_dir import get_default_macro_dir
from ._MacroFile import MacroFile


def load_macro_file(filename: Optional[str] = None) -> Optional[MacroFile]:
    """
    Loads a macro file if one exists.

    :param filename:    The location to load the macro file from,
                        or None to use the default location.
    :return:            The macro file, if one was found.
    """
    # Get the default location if none is provided
    if filename is None:
        filename = os.path.join(get_default_macro_dir(), "macros.json")

    # If the file doesn't exist, return nothing
    if not os.path.exists(filename):
        return None

    # Otherwise load and return the file
    return MacroFile.load_json_from_file(filename)
