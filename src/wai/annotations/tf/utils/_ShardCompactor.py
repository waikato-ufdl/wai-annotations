from typing import Iterable

from ...core import InlineStreamProcessor
from ._sharded_filenames import sharded_filename_params


class ShardCompactor(InlineStreamProcessor[str]):
    """
    Processes the stream of TFRecord files to make sure only
    one shard for each sharded file-set appears.
    """
    def __init__(self):
        # The shard-sets we've already seen
        self._seen = set()

    def _process_element(self, element: str) -> Iterable[str]:
        # Treat the file as a shard file
        base_path, shards, index = sharded_filename_params(element)

        # If it's not a sharded filename, return the file element itself
        if shards == 0:
            return element,

        # If it is a sharded filename, filter it if we've seen in before
        if (base_path, shards) in self._seen:
            return tuple()

        return element,
