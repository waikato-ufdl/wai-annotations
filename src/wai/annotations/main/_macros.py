from wai.common.cli import OptionsList

from ..core.macros import load_macro_file, expand_macros


def perform_macro_expansion(options: OptionsList, filename: str) -> OptionsList:
    """
    Performs macro expansion for the main function.

    :param options:     The stage options supplied to the main function.
    :param filename:    The filename of the macro file specified on the command line.
    :return:            The expanded options.
    """
    # Load the macro file
    macro_file = load_macro_file(None if filename == "" else filename)

    # If a specific macro file was specified and not found, error
    if filename != "" and macro_file is None:
        raise FileNotFoundError(f"Couldn't find macro-file '{filename}'")

    # If the default macro file wasn't found, just continue without macro expansion
    if macro_file is None:
        return options

    return expand_macros(macro_file, options)
