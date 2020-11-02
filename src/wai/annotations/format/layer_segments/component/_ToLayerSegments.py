import numpy as np
from PIL import Image

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image.segmentation import ImageSegmentationInstance
from ..util import LayerSegmentsOutputFormat


class ToLayerSegments(
    RequiresNoFinalisation,
    ProcessorComponent[ImageSegmentationInstance, LayerSegmentsOutputFormat]
):
    """
    Converts the internal image-segmentation format into the one-image-per-label
    annotation format.
    """
    # Multiplier used for packing pixels into bytes
    BYTE_PLACE_MULTIPLIER = np.array([list(1 << i for i in reversed(range(8)))], np.uint8)

    def process_element(
            self,
            element: ImageSegmentationInstance,
            then: ThenFunction[LayerSegmentsOutputFormat],
            done: DoneFunction
    ):
        # Handle negatives
        if element.annotations is None:
            return then(LayerSegmentsOutputFormat(element.data, {}))

        # Create a list of label, segment image pairs
        label_images = {}

        # Process each label separately
        for label_index, label in enumerate(element.annotations.labels, 1):
            # Rows are packed into bytes, so the length must be a multiple of 8
            row_pad = (8 - element.annotations.size[0]) % 8

            # Select the pixels which match this label
            selector_array: np.ndarray = (element.annotations.indices == label_index)

            # If no pixels match this label, no need to create an image
            if not selector_array.any():
                continue

            # Pad the rows
            selector_array = np.pad(selector_array, ((0, 0), (0, row_pad)))

            # Striate the pixels, 8 to a row (includes packing bits)
            selector_array.resize((selector_array.size // 8, 8), refcheck=False)

            # Multiply each applicable bit by its position value in the byte
            selector_array = selector_array * self.BYTE_PLACE_MULTIPLIER

            # Reduce the individual pixels to a byte per group of 8
            selector_array = np.sum(selector_array, 1, np.uint8, keepdims=True)

            # Create the 1-bit image for the label
            annotation = Image.frombytes("1", element.annotations.size, selector_array.tostring())

            # Append the image and its label to the list
            label_images[label] = annotation

        then(
            LayerSegmentsOutputFormat(
                element.data,
                label_images
            )
        )
