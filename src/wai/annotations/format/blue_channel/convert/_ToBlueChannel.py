import numpy as np
from PIL import Image
from typing import Iterator

from ....core.component import OutputConverter
from ....domain.image.segmentation import ImageSegmentationInstance
from .._format import BlueChannelFormat


class ToBlueChannel(OutputConverter[ImageSegmentationInstance, BlueChannelFormat]):
    """
    Converts the internal image-segmentation format into the blue-channel
    annotation format.
    """
    def convert(self, instance: ImageSegmentationInstance) -> Iterator[BlueChannelFormat]:
        # If the number of labels is more than 255, this format can't support it
        if instance.annotations.max_index > 255:
            raise Exception("Indexed PNG supports a maximum of 255 labels")

        # Convert the index array to RGB bytes, with the indices in the blue channel
        rgb_array = np.zeros((*instance.annotations.indices.shape, 3), np.uint8)
        rgb_array[:, :, 2] = instance.annotations.indices.astype(np.uint8)

        # Create the annotation image
        annotation = Image.frombytes("RGB",
                                     instance.annotations.indices.shape,
                                     rgb_array.tostring())

        yield BlueChannelFormat(
            instance.file_info,
            annotation
        )
