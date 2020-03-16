from abc import abstractmethod
from argparse import Namespace
from re import compile
from typing import List, Union, Pattern

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.cli import CLIInstantiable, OptionsList
from wai.common.cli.options import TypedOption

from ..utils import get_object_label
from ..stream import Converter
from .._ImageInfo import ImageInfo
from .._InternalFormat import InternalFormat
from .._typing import ExternalFormat


class InternalFormatConverter(CLIInstantiable, Converter[InternalFormat, ExternalFormat]):
    """
    Base class for converters from the internal format to an external format.
    """
    # The labels that should be included in the output format.
    # If None, use regex matching (see below)
    labels = TypedOption("-l", "--labels",
                         type=str,
                         nargs="+",
                         help="labels to use")

    # The regex to use to select labels to include when an
    # explicit list of labels is not given
    regex = TypedOption("-r", "--regexp",
                        type=str,
                        metavar="regexp",
                        help="regular expression for using only a subset of labels")

    def __init__(self, namespace: Union[Namespace, OptionsList, None] = None):
        super().__init__(namespace)

        self._pattern: Pattern = compile(self.regex) if self.regex is not None else None

    def convert(self, instance: InternalFormat) -> ExternalFormat:
        # Unpack the instance
        image_info, located_objects = instance

        # Use the options to filter the located objects by label
        self.remove_invalid_objects(located_objects)

        return self.convert_unpacked(image_info, located_objects)

    @abstractmethod
    def convert_unpacked(self,
                         image_info: ImageInfo,
                         located_objects: LocatedObjects) -> ExternalFormat:
        """
        Converts an instance from internal format into the external format.

        :param image_info:      The info about the image.
        :param located_objects: The located objects in the image.
        :return:                The instance in external format.
        """
        pass

    def remove_invalid_objects(self, located_objects: LocatedObjects):
        """
        Removes objects with labels that are not valid under the given options.

        :param located_objects:     The located objects to process.
        """
        # Create a list of objects to remove
        invalid_objects: List[int] = []

        # Search the located objects
        for index, located_object in enumerate(located_objects):
            if not self.filter_object(located_object):
                invalid_objects.append(index)

        # Remove the invalid objects
        for index in reversed(invalid_objects):
            located_objects.pop(index)

    def filter_label(self, label: str) -> bool:
        """
        Filter function which selects labels that match the given options.

        :param label:   The label to test.
        :return:        True if the label matches, false if not.
        """
        if len(self.labels) == 0 and self._pattern is None:
            return True
        elif len(self.labels) == 0:
            return bool(self._pattern.match(label))
        elif self._pattern is None:
            return label in self.labels
        else:
            return bool(self._pattern.match(label)) or label in self.labels

    def filter_object(self, located_object: LocatedObject) -> bool:
        """
        Filter function which selects objects whose labels match the given options.

        :param located_object:  The located object to test.
        :return:                True if the object matches, false if not.
        """
        # Filter the label
        return self.filter_label(get_object_label(located_object))
