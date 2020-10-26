import glob
from typing import Iterator


def recursive_iglob(pathname: str) -> Iterator[str]:
    """
    Same as glob.iglob but is always recursive.

    :param pathname:    The path to glob.
    :return:            The globbed path.
    """
    return glob.iglob(pathname, recursive=True)
