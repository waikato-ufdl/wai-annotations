from typing import Optional

from PIL.Image import Image

from ...domain.image import ImageInfo


class IndexedPNGFormat:
    """
    Representation of the indexed-PNG image-segmentation format.
    """
    def __init__(self, image: ImageInfo, annotations: Optional[Image]):
        self._image: ImageInfo = image
        self._annotations: Optional[Image] = annotations

        # Don't need to check annotations for negative images
        if annotations is None:
            return

        # Make sure the two images are the same size
        if image.size is not None and image.size != annotations.size:
            raise Exception("Size of annotations image doesn't match file image size")

        # Make sure the annotation image is an indexed PNG
        if annotations.format != "PNG":
            raise Exception("Annotation image is not a PNG")
        elif annotations.mode != "P":
            raise Exception("Annotation image is not in indexed mode")

    @property
    def image(self) -> ImageInfo:
        return self._image

    @property
    def annotations(self) -> Image:
        return self._annotations
