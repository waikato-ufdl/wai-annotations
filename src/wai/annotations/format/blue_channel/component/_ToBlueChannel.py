import numpy as np
from PIL import Image

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image.segmentation import ImageSegmentationInstance
from ..util import BlueChannelFormat


class ToBlueChannel(
    RequiresNoFinalisation,
    ProcessorComponent[ImageSegmentationInstance, BlueChannelFormat]
):
    """
    Converts the internal image-segmentation format into the blue-channel
    annotation format.
    """
    def process_element(
            self,
            element: ImageSegmentationInstance,
            then: ThenFunction[BlueChannelFormat],
            done: DoneFunction
    ):
        # Create a negative from a negative
        if element.annotations is None:
            return then(BlueChannelFormat(element.data, None))

        # If the number of labels is more than 255, this format can't support it
        if element.annotations.max_index > 255:
            raise Exception("Blue-channel format supports a maximum of 255 labels")

        # Convert the index array to RGB bytes, with the indices in the blue channel
        rgb_array = np.zeros((*element.annotations.indices.shape, 3), np.uint8)
        rgb_array[:, :, 2] = element.annotations.indices.astype(np.uint8)

        # Create the annotation image
        annotation = Image.frombytes("RGB",
                                     element.annotations.size,
                                     rgb_array.tostring())

        then(
            BlueChannelFormat(
                element.data,
                annotation
            )
        )
