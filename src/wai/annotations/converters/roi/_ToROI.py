from argparse import ArgumentParser, Namespace
from typing import Dict, Optional, List, Pattern, Tuple, Any

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from ...core import InternalFormatConverter, ImageInfo
from ...core.constants import LABEL_METADATA_KEY
from ...core.external_formats import ROIExternalFormat, ROIObject


class ToROI(InternalFormatConverter[ROIExternalFormat]):
    """
    Converter from internal format to ROI annotations.
    """
    def __init__(self,
                 labels: Optional[List[str]] = None,
                 regex: Optional[Pattern] = None,
                 image_size: Optional[Tuple[int, int]] = None
                 ):
        super().__init__(labels, regex)

        self.image_size: Optional[Tuple[int, int]] = image_size

        self._label_map: Dict[str, int] = {}

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument(
            "-d", "--image-dimensions", metavar="width,height", dest="image_size", required=False,
            help="image dimensions to use if none can be inferred",
            default="")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(
            image_size=tuple(map(int, namespace.image_size.split(","))) if len(namespace.image_size) > 0 else None
        )
        return kwargs

    def convert_unpacked(self,
                         image_info: ImageInfo,
                         located_objects: LocatedObjects) -> ROIExternalFormat:
        # Make sure we can get the image size
        if image_info.size is not None:
            image_size = image_info.size
        elif self.image_size is not None:
            image_size = self.image_size
        else:
            raise RuntimeError(f"Cannot infer image dimensions for {image_info.filename}")

        # Create a wrapper to convert located objects using the image size
        def convert(located_object: LocatedObject) -> ROIObject:
            return self.convert_located_object(located_object, *image_size)

        return image_info, list(map(convert, located_objects))

    def convert_located_object(self,
                               located_object: LocatedObject,
                               image_width: int,
                               image_height: int) -> ROIObject:
        """
        Converts a located object to ROI format.

        :param located_object:  The located object.
        :param image_width:     The width of the image.
        :param image_height:    The height of the image.
        :return:                The ROI object.
        """
        # Get the object's rectangle
        rectangle = located_object.get_rectangle()

        # Get the object's label
        label = located_object.metadata[LABEL_METADATA_KEY]

        # Add the label to the label map if it's not already present
        if label not in self._label_map:
            self._label_map[label] = len(self._label_map)

        return ROIObject(float(rectangle.left()),
                         float(rectangle.top()),
                         float(rectangle.right()),
                         float(rectangle.bottom()),
                         rectangle.left() / image_width,
                         rectangle.top() / image_height,
                         rectangle.right() / image_width,
                         rectangle.bottom() / image_height,
                         self._label_map[label],
                         label,
                         1.0)
