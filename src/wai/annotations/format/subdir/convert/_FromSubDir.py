from typing import Iterator

from ....core.component import InputConverter
from ....domain.image.classification import ImageClassificationInstance


class FromSubDir(InputConverter[ImageClassificationInstance, ImageClassificationInstance]):
    """
    The sub-dir format uses the internal format as its external format,
    so this is really a pass-through converter.
    """
    def convert(self, instance: ImageClassificationInstance) -> Iterator[ImageClassificationInstance]:
        yield instance
