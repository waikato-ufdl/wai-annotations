import numpy as np

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image.segmentation import ImageSegmentationInstance, ImageSegmentationAnnotation
from ....domain.image.segmentation.util import UnlabelledInputMixin
from ..util import IndexedPNGFormat


class FromIndexedPNG(
    RequiresNoFinalisation,
    UnlabelledInputMixin,
    ProcessorComponent[IndexedPNGFormat, ImageSegmentationInstance]
):
    """
    Converter from the indexed-PNG image-segmentation format
    into the wai.annotations internal format.
    """
    def process_element(
            self,
            element: IndexedPNGFormat,
            then: ThenFunction[ImageSegmentationInstance],
            done: DoneFunction
    ):
        # Create the annotation instance
        annotation = ImageSegmentationAnnotation(self.labels, element.annotations.size)

        # Calculate the indices from the palette indices in the image
        new_indices = np.fromstring(element.annotations.tobytes(), dtype=np.uint8).astype(np.uint16)
        new_indices.resize(annotation.indices.shape)

        # Set the indices to the calculated values
        annotation.indices = new_indices

        then(
            ImageSegmentationInstance(
                element.image,
                annotation
            )
        )
