from typing import Dict

from PIL.Image import Image as PILImage

from ....domain.image import Image


class LayerSegmentsOutputFormat:
    """
    Representation of the one-image-per-label image-segmentation format.
    Only used for the output-converter/writer.
    """
    def __init__(self, image: Image, annotations: Dict[str, PILImage]):
        self._image: Image = image
        self._annotations: Dict[str, PILImage] = annotations

        # Don't need to check annotations for negative images
        if len(annotations) == 0:
            return

        for label, annotation in annotations.items():
            # Make sure the two images are the same size
            if image.size is not None and image.size != annotation.size:
                raise Exception("Size of annotations image doesn't match file image size")

            # Make sure the annotation image is an indexed PNG
            elif annotation.mode != "1":
                raise Exception("Annotation image is not in 1-bit mode")

    @property
    def image(self) -> Image:
        return self._image

    @property
    def annotations(self) -> Dict[str, PILImage]:
        return self._annotations
