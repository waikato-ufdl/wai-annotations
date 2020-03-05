from abc import ABC, abstractmethod
from typing import Iterable

from wai.json.object import JSONObject

from ._SeparateImageWriter import SeparateImageWriter
from ._typing import ExternalFormat


class JSONWriter(SeparateImageWriter[ExternalFormat], ABC):
    """
    Base class for writers that write their annotations out as a single JSON file.
    """
    def __init__(self, output: str, no_images: bool = False, pretty: bool = False):
        super().__init__(output, no_images)

        self.pretty: bool = pretty

    def write_without_images(self, instances: Iterable[ExternalFormat], path: str):
        # Create the JSON object from the instances
        json_object = self.create_json_object(instances)

        # Write the JSON object to disk
        json_object.save_json_to_file(path, 2 if self.pretty else None)

    @abstractmethod
    def create_json_object(self, instances: Iterable[ExternalFormat]) -> JSONObject:
        """
        Creates the JSON object that will be written to disk.

        :param instances:   The instances to write to disk.
        :return:            The JSON object containing the annotations.
        """
        pass

    def expects_file(self) -> bool:
        return True
