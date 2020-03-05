from typing import Optional, Dict, List, Set

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.file.report import Report

from ...core import ExternalFormatConverter, InternalFormat
from ...core.utils import set_object_prefix
from ..utils import find_all_prefixes
from .._format import ADAMSExternalFormat


class FromADAMSReport(ExternalFormatConverter[ADAMSExternalFormat]):
    """
    Converter from ADAMS report-style annotations to internal format.
    """
    def __init__(self,
                 label_mapping: Optional[Dict[str, str]] = None,
                 prefixes: Optional[List[str]] = None):
        super().__init__(label_mapping)

        self.prefixes: Optional[List[str]] = prefixes

    def _convert(self, instance: ADAMSExternalFormat) -> InternalFormat:
        # Unpack the external format
        image_info, report = instance

        # Default to all prefixes if none provided
        prefixes = set(self.prefixes) if self.prefixes is not None else find_all_prefixes(report)

        return image_info, self.get_located_objects_from_report(report, prefixes)

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