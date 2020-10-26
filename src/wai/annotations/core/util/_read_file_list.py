import os
from typing import Iterator


def read_file_list(filename: str) -> Iterator[str]:
    """
    Reads a list of file-names from a file. If a filename
    is relative, it is considered relative to the containing
    file's own location, and is returned with that indirection
    resolved.

    :param filename:    The name of the file containing the file-names.
    :return:            An iterator over the file-names.
    """
    # Get the base directory for the file (for resolving relative paths)
    base_dir = os.path.dirname(filename)

    with open(filename, 'r') as file:
        for line in file.readlines():
            # Strip any leading/training whitespace
            line = line.strip()

            # Remove comments and empty lines
            if line.startswith("#") or line == "":
                continue

            # Resolve relative paths to the containing file's location
            if not line.startswith(os.sep):
                line = os.path.join(base_dir, line)

            yield line.rstrip()
