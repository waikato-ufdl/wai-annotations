from typing import Optional

from PIL.Image import Image as PILImage

from ....domain.image import Image


class BlueChannelFormat:
    """
    Representation of the blue-channel image-segmentation format.
    """
    def __init__(self, image: Image, annotations: Optional[Image]):
        self._image: Image = image
        self._annotations: Optional[PILImage] = annotations

        # Don't need to check annotations for negative images
        if annotations is None:
            return

        # Make sure the two images are the same size
        if image.size is not None and image.size != annotations.size:
            raise Exception("Size of annotations image doesn't match file image size")

    @property
    def image(self) -> Image:
        return self._image

    @property
    def annotations(self) -> PILImage:
        return self._annotations
