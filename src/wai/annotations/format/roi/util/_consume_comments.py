from typing import IO

from ..constants import COMMENT_SYMBOL


def consume_comments(file: IO[str]):
    """
    Reads lines from the file until a non-comment line is found.

    :param file:    The file to read from.
    """
    # Read until end of file
    line = None
    while line != '':
        # Record the position in the file so we can backtrack
        # if we find a non-comment line
        position = file.tell()

        # Read the next line from the file
        line = file.readline()

        # If it's not a comment, backtrack and return
        if not line.startswith(COMMENT_SYMBOL):
            file.seek(position)
            return
