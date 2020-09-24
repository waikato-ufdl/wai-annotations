import numpy as np
from PIL import Image
from typing import Iterator

from ....core.component import OutputConverter
from ....domain.image.segmentation import ImageSegmentationInstance
from .._format import IndexedPNGFormat


class ToIndexedPNG(OutputConverter[ImageSegmentationInstance, IndexedPNGFormat]):
    """
    Converts the internal image-segmentation format into the indexed-PNG
    annotation format.
    """
    def convert(self, instance: ImageSegmentationInstance) -> Iterator[IndexedPNGFormat]:
        # If the number of labels is more than 255, this format can't support it
        if instance.annotations.max_index > 255:
            raise Exception("Indexed PNG supports a maximum of 255 labels")

        # Convert the indices into a palette-index image
        annotation = Image.frombytes("P",
                                     instance.annotations.indices.shape,
                                     instance.annotations.indices.astype(np.uint8).tostring())

        # Add a dummy palette
        # TODO: Allow user to define palette by options
        annotation.putpalette(
            [0, 0, 0,
             255, 0, 0,
             0, 255, 0] + [1 + i // 3 for i in range(759)])

        yield IndexedPNGFormat(
            instance.file_info,
            annotation
        )
