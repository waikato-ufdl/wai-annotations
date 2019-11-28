import re
from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Optional, List, Dict, Any, Pattern, Iterable, Iterator

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from .utils import get_object_label
from .external_formats import ExternalFormat
from ._Converter import Converter
from ._typing import InternalFormat


class InternalFormatConverter(Converter[InternalFormat, ExternalFormat]):
    """
    Base class for converters from the internal format to an external format.
    """
    def __init__(self, labels: Optional[List[str]] = None, regex: Optional[Pattern] = None):
        # The labels that should be included in the output format.
        # If None, use regex matching (see below)
        self.labels: Optional[List[str]] = labels

        # The regex to use to select labels to include when an
        # explicit list of labels is not given
        self.regex: Optional[Pattern] = regex

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.add_argument(
            "-l", "--labels", metavar="label1,label2,...", dest="labels", required=False,
            help="comma-separated list of labels to use", default="")

        parser.add_argument(
            "-r", "--regexp", metavar="regexp", dest="regexp", required=False,
            help="regular expression for using only a subset of labels", default="")

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        # Parse the labels
        labels = list(namespace.labels.split(",")) if len(namespace.labels) > 0 else None

        # Parse the regex
        regex = re.compile(namespace.regexp) if len(namespace.regexp) > 0 else None

        return {"labels": labels, "regex": regex}

    def convert_all(self, instances: Iterable[InternalFormat]) -> Iterator[ExternalFormat]:
        # Filter out any instances that contain no valid labels
        return super().convert_all(filter(self.filter_instance, instances))

    def convert(self, instance: InternalFormat) -> ExternalFormat:
        # Unpack the instance
        image_filename, image_data, located_objects = instance

        # Use the options to filter the located objects by label
        self.remove_invalid_objects(located_objects)

        return self.convert_unpacked(image_filename, image_data, located_objects)

    @abstractmethod
    def convert_unpacked(self,
                         image_filename: str,
                         image_data: Optional[bytes],
                         located_objects: LocatedObjects) -> ExternalFormat:
        """
        Converts an instance from internal format into the external format.

        :param image_filename:  The name of the image file.
        :param image_data:      The binary image data.
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
        if self.labels is not None:
            return label in self.labels
        elif self.regex is not None:
            return bool(self.regex.match(label))
        else:
            return True

    def filter_object(self, located_object: LocatedObject) -> bool:
        """
        Filter function which selects objects whose labels match the given options.

        :param located_object:  The located object to test.
        :return:                True if the object matches, false if not.
        """
        # Filter the label
        return self.filter_label(get_object_label(located_object))

    def filter_instance(self, instance: InternalFormat) -> bool:
        """
        Filter function which selects instances which contain at least one valid located object.

        :param instance:    The instance to test.
        :return:            True if the instance matches, false if not.
        """
        # Get the located objects
        located_objects: LocatedObjects = instance[2]

        return any(self.filter_object(located_object) for located_object in located_objects)
