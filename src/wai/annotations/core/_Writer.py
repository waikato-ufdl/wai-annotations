from abc import abstractmethod
from typing import Generic, Iterable

from ._typing import ExternalFormat


class Writer(Generic[ExternalFormat]):
    """
    Base class for classes which can write a specific external format to disk.
    """
    def __init__(self, output: str):
        super().__init__()

        # The output file/directory to write the converted data-set to
        self.output: str = output

    def save(self, instances: Iterable[ExternalFormat]):
        """
        Writes a series of instances to disk.

        :param instances:   The instances to write to disk.
        """
        self.write(instances, self.output)

    @abstractmethod
    def write(self, instances: Iterable[ExternalFormat], path: str):
        """
        Writes a series of instances to disk.

        :param instances:   The instances to write to disk.
        :param path:        The path to write the instances to. Can be a directory
                            or a specific filename depending on the disk-format
                            of the external format.
        """
        pass
