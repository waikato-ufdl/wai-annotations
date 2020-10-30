from abc import ABC
import os
from typing import List, TypeVar, Optional

from wai.common.cli import OptionValueHandler
from wai.common.cli.options import TypedOption

from ...util import get_associated_image
from ..._ImageFormat import ImageFormat

ExternalFormat = TypeVar("ExternalFormat")


class RelativeDataPathMixin(OptionValueHandler, ABC):
    """
    Mixin which allows the user to specify a relative path to the data images.
    """
    # The relative path to the data image files from the annotation images
    relative_path_to_data_images: List[str] = TypedOption(
        "--image-path-rel",
        type=str,
        metavar="PATH",
        default=".",
        help="Relative path to image files from annotations"
    )

    def get_associated_image(
            self,
            filename: str,
            preference_order: Optional[List[ImageFormat]] = None) -> Optional[str]:
        """
        Gets the data-image associated with the given annotations filename.

        :param filename:            The filename of the annotations file.
        :param preference_order:    The preferred format order in which to search for images.
        :return:                    The filename of the found image, None if not found.
        """
        # Split the filename into path, basename, ext
        path, basename = os.path.split(filename)
        basename, extension = os.path.splitext(basename)

        # Join the path with the relative path to the data-image
        path = os.path.join(path, self.relative_path_to_data_images)

        return get_associated_image(
            os.path.join(path, basename),
            preference_order
        )
