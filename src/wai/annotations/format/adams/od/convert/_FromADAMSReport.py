from typing import Set, Iterator

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.cli.options import TypedOption
from wai.common.file.report import Report

from .....core.component import InputConverter
from .....domain.image.object_detection import ObjectDetectionInstance
from .....domain.image.object_detection.util import set_object_prefix
from ...utils import find_all_prefixes
from ..._format import ADAMSExternalFormat


class FromADAMSReport(InputConverter[ADAMSExternalFormat, ObjectDetectionInstance]):
    """
    Converter from ADAMS report-style annotations to internal format.
    """
    prefixes = TypedOption(
        "-p", "--prefixes",
        type=str,
        nargs="+",
        help="prefixes to parse")

    def convert(self, instance: ADAMSExternalFormat) -> Iterator[ObjectDetectionInstance]:
        # Unpack the external format
        image_info, report = instance

        # Default to all prefixes if none provided
        prefixes = set(self.prefixes) if len(self.prefixes) > 0 else find_all_prefixes(report)

        yield ObjectDetectionInstance(image_info, self.get_located_objects_from_report(report, prefixes))

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
