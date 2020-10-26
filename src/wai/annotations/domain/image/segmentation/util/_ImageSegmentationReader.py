from abc import ABC
import os
from typing import List, TypeVar

from wai.common.cli.options import TypedOption

from .....core.component.util import AnnotationFileProcessor

ExternalFormat = TypeVar("ExternalFormat")


class ImageSegmentationReader(AnnotationFileProcessor[ExternalFormat], ABC):
    """
    Base class for readers of image-segmentation formats.
    """
    # The relative path to the data image files from the annotation images
    relative_path_to_data_images: List[str] = TypedOption(
        "--image-path-rel",
        type=str,
        metavar="PATH",
        default=".",
        help="Relative path to image files from annotations"
    )

    def get_data_path(self, filename: str) -> str:
        """
        Gets the path to the data image associated with a particular
        annotation image.

        :param filename:    The filename of the annotation image.
        :return:            The data-image path.
        """
        # Split the filename from the directory path
        path, annotation_file = os.path.split(filename)

        # Calculate the path to the data files
        return os.path.join(path, self.relative_path_to_data_images)
