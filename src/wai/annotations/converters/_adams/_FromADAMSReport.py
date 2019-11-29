from argparse import ArgumentParser, Namespace
from typing import Optional, Dict, List, Any, Set

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.file.report import Report

from ...core import ExternalFormatConverter, InternalFormat
from ...core.constants import PREFIX_METADATA_KEY
from ...core.external_formats import ADAMSExternalFormat


class FromADAMSReport(ExternalFormatConverter[ADAMSExternalFormat]):
    """
    Converter from ADAMS report-style annotations to internal format.
    """
    def __init__(self,
                 label_mapping: Optional[Dict[str, str]] = None,
                 prefixes: Optional[List[str]] = None):
        super().__init__(label_mapping)

        self.prefixes: Optional[List[str]] = prefixes

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        super().configure_parser(parser)

        parser.add_argument(
            "-p", "--prefixes", metavar="prefix1,prefix2,...", dest="prefixes", required=False,
            help="comma-separated list of prefixes to parse", default="")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        kwargs = super().determine_kwargs_from_namespace(namespace)
        kwargs.update(prefixes=list(namespace.prefixes.split(",")) if len(namespace.prefixes) > 0 else None)
        return kwargs

    def _convert(self, instance: ADAMSExternalFormat) -> InternalFormat:
        # Unpack the external format
        image_info, report = instance

        # Default to all prefixes if none provided
        prefixes = set(self.prefixes) if self.prefixes is not None else self.find_all_prefixes(report)

        return image_info, self.get_located_objects_from_report(report, prefixes)

    def get_located_objects_from_report(self, report: Report, prefixes: Set[str]) -> LocatedObjects:
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
            self.add_prefix_as_metadata(prefix, located_objects_for_prefix)

            # Add the objects to the final set
            located_objects += located_objects_for_prefix

        return located_objects

    def find_all_prefixes(self, report: Report) -> Set[str]:
        """
        Finds all prefixes in the given report.

        :param report:  The report.
        :return:        A set of prefixes in the report.
        """
        # Create the empty set to fill
        prefixes: Set[str] = set()

        # Process all fields for prefixes
        for field in report.get_fields():
            # Get the field name
            name = field.name

            # Extract the prefix if it has one
            if "." in name:
                prefixes.add(name[:name.index(".")])

        return prefixes

    def add_prefix_as_metadata(self, prefix: str, located_objects: LocatedObjects):
        """
        Adds the prefix as a meta-data field to each located object.

        :param prefix:              The prefix.
        :param located_objects:     The located objects.
        """
        for located_object in located_objects:
            located_object.metadata[PREFIX_METADATA_KEY] = prefix
