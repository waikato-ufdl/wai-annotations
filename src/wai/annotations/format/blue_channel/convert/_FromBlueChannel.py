import numpy as np
from typing import Iterator

from ....domain.image.segmentation import ImageSegmentationInstance, ImageSegmentationAnnotation
from ....domain.image.segmentation.util import UnlabelledInputConverter
from .._format import BlueChannelFormat


class FromBlueChannel(UnlabelledInputConverter[BlueChannelFormat]):
    """
    Converter from the blue-channel image-segmentation format
    into the wai.annotations internal format.
    """
    def convert(self, instance: BlueChannelFormat) -> Iterator[ImageSegmentationInstance]:
        # Create the annotation instance
        annotation = ImageSegmentationAnnotation(self.labels, instance.annotations.size)

        # Calculate the indices from the data in the blue channel of the image
        new_indices = instance.annotations.convert("RGB").tobytes()
        new_indices = np.fromstring(new_indices, dtype=np.uint8)
        new_indices.resize((*annotation.indices.shape, 3))
        new_indices = new_indices[:, :, 2]
        new_indices = new_indices.astype(np.uint16)

        # Set the indices to the calculated values
        annotation.indices = new_indices

        yield ImageSegmentationInstance(
            instance.image,
            annotation
        )
