from abc import abstractmethod
from typing import Dict, Optional, Iterable, Iterator

from wai.common.adams.imaging.locateobjects import LocatedObjects

from .utils import get_object_label, set_object_label
from ._typing import InternalFormat
from ._Converter import Converter
from ._DuplicateImageNames import DuplicateImageNames
from ._typing import ExternalFormat


class ExternalFormatConverter(Converter[ExternalFormat, InternalFormat]):
    """
    Base class for converters from an external format to the internal format.
    """
    def __init__(self, label_mapping: Optional[Dict[str, str]] = None):
        super().__init__()

        # An optional mapping to replace/consolidate object labels.
        # The key is the label to replace and the value is the label
        # to replace it with
        self.label_mapping: Optional[Dict[str, str]] = label_mapping

    def convert_all(self, instances: Iterable[ExternalFormat]) -> Iterator[InternalFormat]:
        # Make sure no image is included more than once
        return DuplicateImageNames().process(super().convert_all(instances))

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
            # Get the object's current label
            label: Optional[str] = get_object_label(located_object, True)

            # If the object doesn't have a label, skip it
            if label is None:
                continue

            # If there is a mapping for this label, change it
            if label in self.label_mapping:
                set_object_label(located_object, self.label_mapping[label])
