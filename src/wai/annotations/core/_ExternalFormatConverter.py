from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Dict, Optional, Any

from wai.common.adams.imaging.locateobjects import LocatedObjects

from .external_formats import ExternalFormat
from .constants import LABEL_METADATA_KEY
from ._typing import InternalFormat
from ._Converter import Converter


class ExternalFormatConverter(Converter[ExternalFormat, InternalFormat]):
    """
    Base class for converters from an external format to the internal format.
    """
    def __init__(self, label_mapping: Optional[Dict[str, str]] = None):
        # An optional mapping to replace/consolidate object labels.
        # The key is the label to replace and the value is the label
        # to replace it with
        self.label_mapping: Optional[Dict[str, str]] = label_mapping

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.add_argument(
            "-m", "--mapping", metavar="old=new", dest="mapping", action='append', type=str, required=False,
            help="mapping for labels, for replacing one label string with another (eg when fixing/collapsing labels)",
            default=list())

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        # Create the empty mapping
        mapping = {}

        # Add each provided exchange to the mapping
        for map_string in namespace.mapping:
            old, new = map_string.split("=")

            # Make sure we don't double-map a label
            if old in mapping:
                raise ValueError(f"Multiple mappings specified for label '{old}'")

            mapping[old] = new

        return {"label_mapping": mapping}

    def convert(self, instance: ExternalFormat) -> InternalFormat:
        # Do the conversion
        converted_instance: InternalFormat = self._convert(instance)

        # Unpack the converted instance
        image_info, located_objects = converted_instance

        # Apply the label mapping
        self.apply_label_mapping(located_objects)

        return converted_instance

    @abstractmethod
    def _convert(self, instance: ExternalFormat) -> InternalFormat:
        """
        Converts an instance in external format into the internal format.

        :param instance:    The instance in external format.
        :return:            The instance in internal format.
        """
        pass

    def apply_label_mapping(self, located_objects: LocatedObjects):
        """
        Maps the labels in the located objects from their current value to
        their new value.

        :param located_objects:     The parsed objects
        """
        # Do nothing if no mapping provided
        if self.label_mapping is None:
            return

        # Process each object
        for located_object in located_objects:
            # If the object doesn't have a label, skip it
            if LABEL_METADATA_KEY not in located_object.metadata:
                continue

            # Get the object's current label
            label: str = located_object.metadata[LABEL_METADATA_KEY]

            # If there is a mapping for this label, change it
            if label in self.label_mapping:
                located_object.metadata[LABEL_METADATA_KEY] = self.label_mapping[label]
