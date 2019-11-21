import re
from typing import Tuple, Pattern

# Pattern for matching sharded record filenames
SHARDED_FILENAME_PATTERN: Pattern = re.compile("^(.*)-(\\d{5})-of-(\\d{5})$")


def format_sharded_filename(base_name: str, shards: int, index: int):
    """
    Formats the filename for a shard in sharded output.

    :param base_name:   The base filename to use.
    :param shards:      The number of shards being output, total.
    :param index:       The index of the current shard [0:shards).
    :return:            The formatted filename.
    """
    return f"{base_name}-{index:05}-of-{shards:05}"


def sharded_filename_params(filename: str) -> Tuple[str, int, int]:
    """
    Gets the base path, number of shards and shard index
    from a sharded filename.

    :param filename:    The filename to process.
    :return:            The base name, the number of shards,
                        and the shard index.
    """
    match = SHARDED_FILENAME_PATTERN.match(filename)

    if match:
        return match.group(1), int(match.group(3)), int(match.group(2))
    else:
        return "", 0, 0
