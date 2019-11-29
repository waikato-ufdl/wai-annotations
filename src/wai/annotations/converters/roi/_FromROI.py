from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from ...core import ExternalFormatConverter, InternalFormat
from ...core.constants import PREFIX_METADATA_KEY, LABEL_METADATA_KEY, DEFAULT_PREFIX
from ...core.external_formats import ROIExternalFormat, ROIObject


class FromROI(ExternalFormatConverter[ROIExternalFormat]):
    """
    Converter from ROI CSV annotations to internal format.
    """
    def _convert(self, instance: ROIExternalFormat) -> InternalFormat:
        # Unpack the external format
        image_info, roi_objects = instance

        return image_info, LocatedObjects(map(self.convert_roi_object, roi_objects))

    def convert_roi_object(self, roi_object: ROIObject) -> LocatedObject:
        """
        Converts a ROI object to an internal-format located object.

        :param roi_object:  The ROI object to convert.
        :return:            The located object.
        """
        return LocatedObject(round(roi_object.x0),
                             round(roi_object.y0),
                             round(roi_object.x1 - roi_object.x0),
                             round(roi_object.y1 - roi_object.y0),
                             **{LABEL_METADATA_KEY: roi_object.label_str,
                                PREFIX_METADATA_KEY: DEFAULT_PREFIX})
