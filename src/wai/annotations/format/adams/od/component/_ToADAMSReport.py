from wai.common.file.report import Report

from .....core.component import ProcessorComponent
from .....core.stream import ThenFunction, DoneFunction
from .....core.stream.util import RequiresNoFinalisation
from .....domain.image.object_detection import ImageObjectDetectionInstance
from ...util import divide_by_prefix, remove_prefix_metadata, ADAMSExternalFormat


class ToADAMSReport(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, ADAMSExternalFormat]
):
    """
    Converter from internal format to ADAMS report-style annotations.
    """
    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[ADAMSExternalFormat],
            done: DoneFunction
    ):
        image_info, located_objects = element

        # If no located objects were found, return a negative instance
        if located_objects is None or len(located_objects) == 0:
            then((image_info, None))

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

            then((image_info, report))
