from typing import Set

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.cli.options import TypedOption
from wai.common.file.report import Report

from .....core.component import ProcessorComponent
from .....core.stream import ThenFunction, DoneFunction
from .....core.stream.util import RequiresNoFinalisation
from .....domain.image.object_detection import ImageObjectDetectionInstance
from .....domain.image.object_detection.util import set_object_prefix
from ...util import find_all_prefixes, ADAMSExternalFormat


class FromADAMSReport(
    RequiresNoFinalisation,
    ProcessorComponent[ADAMSExternalFormat, ImageObjectDetectionInstance]
):
    """
    Converter from ADAMS report-style annotations to internal format.
    """
    prefixes = TypedOption(
        "-p", "--prefixes",
        type=str,
        nargs="+",
        help="prefixes to parse")

    def process_element(self, element: ADAMSExternalFormat, then: ThenFunction[ImageObjectDetectionInstance], done: DoneFunction):
        # Unpack the external format
        image_info, report = element

        # Extract the located objects from the report if present
        located_objects = None
        if report is not None:
            # Default to all prefixes if none provided
            prefixes = set(self.prefixes) if len(self.prefixes) > 0 else find_all_prefixes(report)
            located_objects = self.get_located_objects_from_report(report, prefixes)

        then(
            ImageObjectDetectionInstance(
                image_info,
                located_objects
            )
        )

    @staticmethod
    def get_located_objects_from_report(report: Report, prefixes: Set[str]) -> LocatedObjects:
        """
        Gets the located objects with one of the given prefixes from a report.

        :param report:      The report to extract objects from.
        :param prefixes:    The prefixes to extract objects for.
        :return:            The objects.
        """
        # Create an empty set of objects
        located_objects = LocatedObjects()

        # Process objects for each prefix
        for prefix in prefixes:
            # Get the objects with this prefix
            located_objects_for_prefix = LocatedObjects.from_report(report, prefix)

            # Add the prefix to the meta-data of the objects
            for located_object in located_objects_for_prefix:
                set_object_prefix(located_object, prefix)

            # Add the objects to the final set
            located_objects += located_objects_for_prefix

        return located_objects
