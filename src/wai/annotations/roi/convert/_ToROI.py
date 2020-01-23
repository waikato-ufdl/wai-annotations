from typing import Dict, Optional, List, Pattern, Tuple

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from ...core import InternalFormatConverter, ImageInfo
from ...core.utils import get_object_label, get_object_prefix, get_object_metadata
from .._format import ROIExternalFormat
from .._min_rect_from_roi_polygon import min_rect_from_roi_polygon
from .._roi_polygon import roi_polygon
from .._ROIObject import ROIObject


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
        label = get_object_label(located_object)

        # Add the label to the label map if it's not already present
        if label not in self._label_map:
            self._label_map[label] = len(self._label_map)

        # Create keyword arguments from the required attributes
        kwargs = dict(x0=float(rectangle.left()),
                      y0=float(rectangle.top()),
                      x1=float(rectangle.right()),
                      y1=float(rectangle.bottom()),
                      x0n=rectangle.left() / image_width,
                      y0n=rectangle.top() / image_height,
                      x1n=rectangle.right() / image_width,
                      y1n=rectangle.bottom() / image_height,
                      label=self._label_map[label],
                      label_str=label,
                      score=1.0)

        # If there is a polygon, add them as keyword arguments
        if located_object.has_polygon():
            poly_x, poly_y = roi_polygon(located_object.get_polygon())
            minrect_w, minrect_h = min_rect_from_roi_polygon(poly_x, poly_y)
            kwargs.update(poly_x=poly_x,
                          poly_y=poly_y,
                          poly_xn=list(map(lambda x: x / image_width, poly_x)),
                          poly_yn=list(map(lambda y: y / image_height, poly_y)),
                          minrect_w=minrect_w,
                          minrect_h=minrect_h)

        # Set the non-standard keywords
        prefix = get_object_prefix(located_object, True)
        if prefix is not None:
            kwargs.update(prefix=prefix)
        kwargs.update(**get_object_metadata(located_object))

        return ROIObject(**kwargs)
