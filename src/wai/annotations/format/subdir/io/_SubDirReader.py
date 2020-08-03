import os
from typing import Iterator

from ....core.component import LocalReader
from ....domain.image import ImageInfo
from ....domain.image.classification import ImageClassificationInstance


class SubDirReader(LocalReader[ImageClassificationInstance]):
    """
    Reader of image-classification datasets which store images in
    folders named after the classification label.
    """
    def read_annotation_file(self, filename: str) -> Iterator[ImageClassificationInstance]:
        # The label is the last directory folder of the filename
        label = os.path.basename(os.path.dirname(filename))

        yield ImageClassificationInstance(
            ImageInfo.from_file(filename),
            label
        )

    def read_negative_file(self, filename: str) -> Iterator[ImageClassificationInstance]:
        yield ImageClassificationInstance(
            ImageInfo.from_file(filename),
            ""
        )
