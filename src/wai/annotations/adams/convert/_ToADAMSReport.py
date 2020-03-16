from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.file.report import Report

from ...core import ImageInfo
from ...core.components import InternalFormatConverter
from .._format import ADAMSExternalFormat
from ..utils import divide_by_prefix, remove_prefix_metadata


class ToADAMSReport(InternalFormatConverter[ADAMSExternalFormat]):
    """
    Converter from internal format to ADAMS report-style annotations.
    """
    def convert_unpacked(self,
                         image_info: ImageInfo,
                         located_objects: LocatedObjects) -> ADAMSExternalFormat:
        # If no located objects were found, return an empty report
        if len(located_objects) == 0:
            return image_info, located_objects.to_report()

        # Divide the located objects into unique prefixes
        prefix_objects = divide_by_prefix(located_objects)

        # Remove the prefix meta-data as it will be written as the actual prefix
        remove_prefix_metadata(located_objects)

        # Create reports from each set of objects
        prefix_reports = [objects.to_report(prefix) for prefix, objects in prefix_objects.items()]

        # Merge the reports into a final report
        report: Report = prefix_reports[0]
        for prefix_report in prefix_reports[1:]:
            report.merge_with(prefix_report)

        return image_info, report
