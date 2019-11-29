from typing import Dict, Optional, List, Pattern

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from ...core import InternalFormatConverter, ImageInfo
from ...core.constants import LABEL_METADATA_KEY
from ...core.external_formats import ROIExternalFormat, ROIObject


class ToROI(InternalFormatConverter[ROIExternalFormat]):
    """
    Converter from internal format to ROI annotations.
    """
    def __init__(self, labels: Optional[List[str]] = None, regex: Optional[Pattern] = None):
        super().__init__(labels, regex)

        self._label_map: Dict[str, int] = {}

    def convert_unpacked(self,
                         image_info: ImageInfo,
                         located_objects: LocatedObjects) -> ROIExternalFormat:
        return image_info, list(map(self.convert_located_object, located_objects))

    def convert_located_object(self, located_object: LocatedObject) -> ROIObject:
        """
        Converts a located object to ROI format.

        :param located_object:  The located object.
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
                         rectangle.left() / rectangle.width(),
                         rectangle.top() / rectangle.height(),
                         rectangle.right() / rectangle.width(),
                         rectangle.bottom() / rectangle.height(),
                         self._label_map[label],
                         label,
                         1.0)
