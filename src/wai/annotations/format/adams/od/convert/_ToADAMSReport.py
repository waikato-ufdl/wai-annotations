from typing import Iterator

from wai.common.file.report import Report

from .....core.component import OutputConverter
from .....domain.image.object_detection import ObjectDetectionInstance
from ...utils import divide_by_prefix, remove_prefix_metadata
from ..._format import ADAMSExternalFormat


class ToADAMSReport(OutputConverter[ObjectDetectionInstance, ADAMSExternalFormat]):
    """
    Converter from internal format to ADAMS report-style annotations.
    """
    def convert(self, instance: ObjectDetectionInstance) -> Iterator[ADAMSExternalFormat]:
        image_info, located_objects = instance

        # If no located objects were found, return an empty report
        if len(located_objects) == 0:
            yield image_info, located_objects.to_report()

        else:
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

            yield image_info, report
