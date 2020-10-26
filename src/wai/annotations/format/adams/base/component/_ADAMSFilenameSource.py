import os
from typing import Tuple, Iterator

from .....core.component.util import LocalFilenameSource
from .....core.util import InstanceState, recursive_iglob
from ...constants import DEFAULT_EXTENSION


class ADAMSFilenameSource(LocalFilenameSource):
    input_file_names: Tuple[str, ...] = InstanceState(lambda self: tuple(self.add_reports_from_directory()))

    def add_reports_from_directory(self) -> Iterator[str]:
        # Further process the set of annotation files
        for file in super().input_file_names:
            # If the file is a directory, default to all files that end in the default extension
            if os.path.isdir(file):
                for filename in recursive_iglob(os.path.join(file, f"*{DEFAULT_EXTENSION}")):
                    yield filename

            # Otherwise read the file as normal
            else:
                yield file
