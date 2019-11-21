from wai.common.adams.imaging.locateobjects import LocatedObjects

from ...core import InternalFormatConverter, ImageFormat
from ...core.external_formats import ADAMSExternalFormat


class ToADAMSReport(InternalFormatConverter[ADAMSExternalFormat]):
    """
    Converter from internal format to ADAMS report-style annotations.
    """
    def convert_unpacked(self,
                         image_filename: str,
                         image_data: bytes,
                         image_format: ImageFormat,
                         located_objects: LocatedObjects) -> ADAMSExternalFormat:
        return image_filename, image_data, image_format, located_objects.to_report()
