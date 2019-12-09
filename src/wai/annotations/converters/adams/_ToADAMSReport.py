from typing import Dict

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.file.report import Report

from ...core import InternalFormatConverter, ImageInfo
from ...core.constants import PREFIX_METADATA_KEY
from ...core.external_formats import ADAMSExternalFormat


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
        prefix_objects = self.divide_by_prefix(located_objects)

        # Remove the prefix meta-data as it will be written as the actual prefix
        self.remove_prefix_metadata(located_objects)

        # Create reports from each set of objects
        prefix_reports = [objects.to_report(prefix) for prefix, objects in prefix_objects.items()]

        # Merge the reports into a final report
        report: Report = prefix_reports[0]
        for prefix_report in prefix_reports[1:]:
            report.merge_with(prefix_report)

        return image_info, report

    def divide_by_prefix(self, located_objects: LocatedObjects) -> Dict[str, LocatedObjects]:
        """
        Divides a single set of located objects into sub-sets where
        each shares a common prefix.

        :param located_objects:     The located objects.
        :return:                    Map from prefix to located objects with that prefix.
        """
        # Create the empty map
        prefix_objects: Dict[str, LocatedObjects] = {}

        # Process each object into the map
        for located_object in located_objects:
            # Get the object's prefix
            prefix: str = located_object.metadata[PREFIX_METADATA_KEY]

            # Create a new group for the prefix the first time we encounter it
            if prefix not in prefix_objects:
                prefix_objects[prefix] = LocatedObjects()

            # Add the object to its prefix group
            prefix_objects[prefix].append(located_object)

        return prefix_objects

    def remove_prefix_metadata(self, located_objects: LocatedObjects):
        """
        Removes the prefix meta-data from the located objects.

        :param located_objects:     The located objects.
        """
        for located_object in located_objects:
            if PREFIX_METADATA_KEY in located_object.metadata:
                del located_object.metadata[PREFIX_METADATA_KEY]
