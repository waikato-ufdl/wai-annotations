import re


def extension_to_regex(extension: str) -> str:
    """
    Converts an extension into a regex which matches
    filenames with that extension.

    :param extension:   The extension.
    :return:            A pattern object.
    """
    # Escape the extension and format it as a regex
    return f"(.*){re.escape(extension)}$"
