from wai.common.adams.imaging.locateobjects import LocatedObjects

from ...core import ExternalFormatConverter, InternalFormat
from ...core.external_formats import ADAMSExternalFormat


class FromADAMSReport(ExternalFormatConverter[ADAMSExternalFormat]):
    """
    Converter from ADAMS report-style annotations to internal format.
    """
    def _convert(self, instance: ADAMSExternalFormat) -> InternalFormat:
        # Unpack the external format
        image_filename, image_data, image_format, report = instance

        # Get the located objects from the report
        located_objects = LocatedObjects.from_report(report)

        return image_filename, image_data, image_format, located_objects
