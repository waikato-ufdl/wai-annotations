import os
from typing import Iterable


def get_files_from_directory(directory: str, extension: str = "") -> Iterable[str]:
    """
    Recursively gets files from all sub-directories of the
    given directory (including itself).

    :param directory:   The top-level directory to search.
    :param extension:   The extension to limit files to.
    :return:            The iterator of filenames.
    """
    # Process each subdirectory
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(subdir, file)
