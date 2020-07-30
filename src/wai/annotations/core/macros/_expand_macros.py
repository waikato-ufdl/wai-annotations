from itertools import chain
from typing import Optional, List

from wai.common.cli import OptionsList

from ._MacroFile import MacroFile


def expand_macros(macros: MacroFile, options: OptionsList) -> OptionsList:
    """
    Returns the options list, with macros from the given file expanded.

    :param macros:      The file of macros to expand.
    :param options:     The options list (including macros).
    :return:            An options list with macros expanded.
    """
    return join_options(map_macros(macros, options))


def map_macros(macros: MacroFile, options: OptionsList, seen: Optional[List[str]] = None) -> List[OptionsList]:
    """
    Performs recursive expansion of macros, mapping each input option to its
    expanded list of options (or just the original option if no expansion is
    found).

    :param macros:      The macro file to expand macros from.
    :param options:     The original options list.
    :param seen:        A stack of seen macros in this branch of the recursion
                        (for cycle detection).
    :return:            A list of expanded options.
    """
    # Create a result list
    result = []

    # Process each option in sequence
    for option in options:
        # If there isn't a macro for the option, just direct it to the result as-is
        if not macros.has_property(option):
            result.append([option])

        # Otherwise recursively expand the macro
        else:
            # Calculate the new stack of seen macros
            new_seen = [option] if seen is None else seen + [option]

            # Check for cyclic macros
            if seen is not None and option in seen:
                raise Exception("Cyclic macro expansion encountered: " + " -> ".join(new_seen))

            # Recurse, flatten and append
            result.append(join_options(map_macros(macros, macros.get_property(option), new_seen)))

    return result


def join_options(options: List[OptionsList]) -> OptionsList:
    """
    Joins a list of options lists into a single options list.

    :param options:     The list of options lists.
    :return:            The joined options list.
    """
    return list(chain.from_iterable(options))
