from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from ...core import ExternalFormatConverter, InternalFormat
from ...core.utils import set_object_label, set_object_metadata, set_object_prefix
from .._format import ROIExternalFormat
from ..utils import polygon_from_roi_object
from .._ROIObject import ROIObject


class FromROI(ExternalFormatConverter[ROIExternalFormat]):
    """
    Converter from ROI CSV annotations to internal format.
    """
    def _convert(self, instance: ROIExternalFormat) -> InternalFormat:
        # Unpack the external format
        image_info, roi_objects = instance

        return image_info, LocatedObjects(map(self.convert_roi_object, roi_objects))

    @staticmethod
    def convert_roi_object(roi_object: ROIObject) -> LocatedObject:
        """
        Converts a ROI object to an internal-format located object.

        :param roi_object:  The ROI object to convert.
        :return:            The located object.
        """
        located_object = LocatedObject(round(roi_object.x0),
                                       round(roi_object.y0),
                                       round(roi_object.x1 - roi_object.x0),
                                       round(roi_object.y1 - roi_object.y0))

        set_object_label(located_object, roi_object.label_str)

        # Set any non-standard keywords as meta-data
        metadata = roi_object.non_standard_kwargs.copy()
        if "prefix" in metadata:
            set_object_prefix(located_object, metadata["prefix"])
            del metadata["prefix"]
        set_object_metadata(located_object, **metadata)

        # Add the polygon
        if roi_object.has_polygon():
            located_object.set_polygon(polygon_from_roi_object(roi_object))

        return located_object
