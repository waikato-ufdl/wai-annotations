import os
from typing import Iterable, Pattern


def get_files_from_directory(directory: str, pattern: Pattern) -> Iterable[str]:
    """
    Recursively gets files from all sub-directories of the
    given directory (including itself).

    :param directory:   The top-level directory to search.
    :param pattern:     The pattern to match filenames.
    :return:            The iterator of filenames.
    """
    # Process each subdirectory
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if pattern.match(file):
                yield os.path.join(subdir, file)
