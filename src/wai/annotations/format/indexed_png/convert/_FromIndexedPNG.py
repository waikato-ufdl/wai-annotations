import numpy as np
from typing import Iterator

from ....domain.image.segmentation import ImageSegmentationInstance, ImageSegmentationAnnotation
from ....domain.image.segmentation.util import UnlabelledInputConverter
from .._format import IndexedPNGFormat


class FromIndexedPNG(UnlabelledInputConverter[IndexedPNGFormat]):
    """
    Converter from the indexed-PNG image-segmentation format
    into the wai.annotations internal format.
    """
    def convert(self, instance: IndexedPNGFormat) -> Iterator[ImageSegmentationInstance]:
        # Create the annotation instance
        annotation = ImageSegmentationAnnotation(self.labels, instance.annotations.size)

        # Calculate the indices from the palette indices in the image
        new_indices = np.fromstring(instance.annotations.tobytes(), dtype=np.uint8).astype(np.uint16)
        new_indices.resize(annotation.indices.shape)

        # Set the indices to the calculated values
        annotation.indices = new_indices

        yield ImageSegmentationInstance(
            instance.image,
            annotation
        )
