import numpy as np

from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image.segmentation import ImageSegmentationInstance, ImageSegmentationAnnotation
from ....domain.image.segmentation.util import UnlabelledInputConverter
from ..util import BlueChannelFormat


class FromBlueChannel(
    RequiresNoFinalisation,
    UnlabelledInputConverter[BlueChannelFormat]
):
    """
    Converter from the blue-channel image-segmentation format
    into the wai.annotations internal format.
    """
    def process_element(
            self,
            element: BlueChannelFormat,
            then: ThenFunction[ImageSegmentationInstance],
            done: DoneFunction
    ):
        # Create the annotation instance
        annotation = ImageSegmentationAnnotation(self.labels, element.annotations.size)

        # Calculate the indices from the data in the blue channel of the image
        new_indices = element.annotations.convert("RGB").tobytes()
        new_indices = np.fromstring(new_indices, dtype=np.uint8)
        new_indices.resize((*annotation.size, 3))
        new_indices = new_indices[:, :, 2]
        new_indices = new_indices.astype(np.uint16)

        # Set the indices to the calculated values
        annotation.indices = new_indices

        then(
            ImageSegmentationInstance(
                element.image,
                annotation
            )
        )
