from abc import abstractmethod
from argparse import Namespace
from typing import Optional, Iterable, Iterator, Union

from wai.common.adams.imaging.locateobjects import LocatedObjects
from wai.common.cli import CLIInstantiable, OptionsList
from wai.common.cli.options import TypedOption

from ..utils import get_object_label, set_object_label
from ..stream import Converter
from .._InternalFormat import InternalFormat
from .._DuplicateImageNames import DuplicateImageNames
from .._typing import ExternalFormat


class ExternalFormatConverter(CLIInstantiable, Converter[ExternalFormat, InternalFormat]):
    """
    Base class for converters from an external format to the internal format.
    """
    # An optional mapping to replace/consolidate object labels.
    # The key is the label to replace and the value is the label
    # to replace it with
    label_mapping = TypedOption(
        "-m", "--mapping",
        type=str,
        metavar="old=new", action='append',
        help="mapping for labels, for replacing one label string with another (eg when fixing/collapsing labels)"
    )

    def __init__(self, namespace: Union[Namespace, OptionsList, None] = None):
        super().__init__(namespace)

        # Create the label mapping
        self._label_mapping = {}
        for map_string in self.label_mapping:
            old, new = map_string.split("=")

            # Make sure we don't double-map a label
            if old in self._label_mapping:
                raise ValueError(f"Multiple mappings specified for label '{old}': "
                                 f"{self._label_mapping[old]}, {new}")

            self._label_mapping[old] = new

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
        if len(self._label_mapping) == 0:
            return

        # Process each object
        for located_object in located_objects:
            # Get the object's current label
            label: Optional[str] = get_object_label(located_object, None)

            # If the object doesn't have a label, skip it
            if label is None:
                continue

            # If there is a mapping for this label, change it
            if label in self._label_mapping:
                set_object_label(located_object, self._label_mapping[label])
