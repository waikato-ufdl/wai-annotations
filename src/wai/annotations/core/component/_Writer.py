from abc import abstractmethod
from typing import Generic, Iterable, TypeVar

from wai.bynning.operations import split as bynning_split_op

from wai.common.cli import CLIInstantiable
from wai.common.cli.options import TypedOption

from ..instance import FileInfo
from ..logging import LoggingEnabled, StreamLogger

ExternalFormat = TypeVar("ExternalFormat")


class Writer(LoggingEnabled, CLIInstantiable, Generic[ExternalFormat]):
    """
    Base class for classes which can write a specific external format.
    """
    split_names = TypedOption("--split-names",
                              type=str,
                              metavar="SPLIT NAME",
                              nargs="+",
                              help="the names to use for the splits")

    split_ratios = TypedOption("--split-ratios",
                               type=int,
                               metavar="RATIO",
                               nargs="+",
                               help="the ratios to use for the splits")

    @property
    def is_splitting(self) -> bool:
        """
        Whether this writer is performing a split-write.
        """
        return len(self.split_names) != 0 and len(self.split_ratios) != 0

    def save(self, instances: Iterable[ExternalFormat]):
        """
        Writes a series of instances to disk.

        :param instances:   The instances to write to disk.
        """
        # Create a stream processor to log when we are writing a file
        stream_logger = StreamLogger(
            self.logger.info,
            lambda instance:
            f"Saving annotations for "
            f"{self.extract_file_info_from_external_format(instance).filename}")

        # If creating a split, defer to wai.bynning
        if self.is_splitting:
            # Split and iterate through the instances for the split
            for split_name, split_instances in bynning_split_op(
                    instances,
                    **{split_name: split_ratio
                       for split_name, split_ratio
                       in zip(self.split_names, self.split_ratios)}
            ).items():
                # Write the split
                self.split_write(stream_logger.process(split_instances), split_name)

        # Otherwise just write the instances
        else:
            self.write(stream_logger.process(instances))

    @abstractmethod
    def split_write(self, instances: Iterable[ExternalFormat], split_name: str):
        """
        Writes a series of instances to disk as part of a single split.

        :param instances:   The instances to write for the split.
        :param split_name:  The name of the split.
        """
        pass

    @abstractmethod
    def write(self, instances: Iterable[ExternalFormat]):
        """
        Writes a series of instances to disk.

        :param instances:   The instances to write to disk.
        """
        pass

    @abstractmethod
    def extract_file_info_from_external_format(self, instance: ExternalFormat) -> FileInfo:
        """
        Extracts a file-info object from the external format of this writer.

        :param instance:    The instance being written.
        :return:            The file-info for the instance.
        """
        pass
