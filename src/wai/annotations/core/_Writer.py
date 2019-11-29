from abc import abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Generic, Iterable, Dict, Any

from .external_formats import ExternalFormat
from ._ArgumentConsumer import ArgumentConsumer


class Writer(ArgumentConsumer, Generic[ExternalFormat]):
    """
    Base class for classes which can write a specific external format to disk.
    """
    def __init__(self, output: str):
        self.output: str = output

    @classmethod
    def configure_parser(cls, parser: ArgumentParser):
        parser.add_argument(
            "-o", "--output", metavar="dir_or_file", dest="output", required=True,
            help=cls.output_help_text())

    @classmethod
    def determine_kwargs_from_namespace(cls, namespace: Namespace) -> Dict[str, Any]:
        return {"output": namespace.output}

    @classmethod
    @abstractmethod
    def output_help_text(cls) -> str:
        """
        Gets the help text describing what type of path the 'output' option
        expects and how it is interpreted.

        :return:    The help text.
        """
        pass

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
