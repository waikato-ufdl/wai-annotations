import numpy as np
from PIL import Image

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image.segmentation import ImageSegmentationInstance
from ..util import IndexedPNGFormat


class ToIndexedPNG(
    RequiresNoFinalisation,
    ProcessorComponent[ImageSegmentationInstance, IndexedPNGFormat]
):
    """
    Converts the internal image-segmentation format into the indexed-PNG
    annotation format.
    """
    def process_element(
            self,
            element: ImageSegmentationInstance,
            then: ThenFunction[IndexedPNGFormat],
            done: DoneFunction
    ):
        # If the element is a negative, forward it as such
        if element.annotations is None:
            return then(IndexedPNGFormat(element.data, None))

        # If the number of labels is more than 255, this format can't support it
        if element.annotations.max_index > 255:
            raise Exception("Indexed PNG supports a maximum of 255 labels")

        # Convert the indices into a palette-index image
        annotation = Image.frombytes(
            "P",
            element.annotations.size,
            element.annotations.indices.astype(np.uint8).tostring()
        )

        # Add a dummy palette
        # TODO: Allow user to define palette by options
        annotation.putpalette(
            [0, 0, 0,
             255, 0, 0,
             0, 255, 0] + [1 + i // 3 for i in range(759)])

        then(
            IndexedPNGFormat(
                element.data,
                annotation
            )
        )
