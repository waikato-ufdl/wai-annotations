from argparse import Namespace
import os
from abc import abstractmethod, abstractproperty
from tempfile import TemporaryDirectory
from typing import Optional, TypeVar, Iterator, IO, Tuple, Iterable

from wai.common.cli.options import TypedOption, Option

from ...stream import Pipeline
from .._SinkComponent import SinkComponent

ElementType = TypeVar("ElementType")


class LocalFileWriter(SinkComponent[ElementType]):
    """
    Base class for classes which can write a specific external format to disk.
    """
    # The file or directory to write into
    output = TypedOption(
        "-o", "--output",
        type=str,
        metavar="PATH",
        required=True
    )

    @property
    def output_path(self) -> str:
        """
        The directory this writer is writing to.
        """
        # Get the path from the 'output' option
        output_path = os.path.abspath(self.output)
        if self.expects_file:
            output_path = os.path.dirname(output_path)

        # Make sure the path ends with a slash
        if not output_path.endswith(os.path.sep):
            output_path += os.path.sep

        return output_path

    @classmethod
    def get_help_text_for_option(cls, option: Option) -> Optional[str]:
        if option is cls.output:
            return cls.get_help_text_for_output_option()
        return super().get_help_text_for_option(option)

    @classmethod
    @abstractmethod
    def get_help_text_for_output_option(cls) -> str:
        """
        Gets the help text describing what type of path the 'output' option
        expects and how it is interpreted.

        :return:    The help text.
        """
        raise NotImplementedError(cls.get_help_text_for_option.__qualname__)

    @abstractproperty
    def expects_file(self) -> bool:
        """
        Whether this writer expects the 'output' option to specify
        a file, or if not, a directory.
        """
        raise NotImplementedError(type(self).expects_file.__qualname__)


class ExpectsFile:
    """
    Mixin class which declares the local file-writer expects a file-name
    for its 'output' option.
    """
    @property
    def expects_file(self) -> bool:
        return True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not issubclass(cls, LocalFileWriter):
            raise Exception(
                f"{ExpectsFile.__qualname__} can only be used in conjunction "
                f"with the {LocalFileWriter.__qualname__} class"
            )


class ExpectsDirectory:
    """
    Mixin class which declares the local file-writer expects a directory-name
    for its 'output' option.
    """
    @property
    def expects_file(self) -> bool:
        return False

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not issubclass(cls, LocalFileWriter):
            raise Exception(
                f"{ExpectsDirectory.__qualname__} can only be used in conjunction "
                f"with the {LocalFileWriter.__qualname__} class"
            )


def iterate_files(pipeline: Pipeline, source: Optional[Iterable] = None) -> Iterator[Tuple[str, IO[bytes]]]:
    """
    Iterates through the files written by a pipeline.

    :param pipeline:    The pipeline (must end in a local file-writer).
    :param source:      The source to provide stream elements to the pipeline.
                        Uses the fixed source if none given.
    :return:            An iterator of file-name, file pairs.
    """
    # Get the writer from the end of the pipeline
    writer = pipeline.sink

    # Make sure the pipeline ends with a local file-writer
    if not isinstance(writer, LocalFileWriter):
        raise Exception(
            "Can only iterate files for pipelines that end in "
            "a local file-writer"
        )

    # Create a temporary directory to write into
    with TemporaryDirectory() as temp_directory:
        # Format a new output location within the temp directory
        new_output = (
            temp_directory
            if not writer.expects_file
            else os.path.join(temp_directory, os.path.basename(writer.output))
        )

        # Create a clone of the writer with the new output
        temp_writer = type(writer)(Namespace(**vars(writer.namespace)))
        temp_writer.output = new_output

        # Create a new pipeline with the new output
        new_pipeline = Pipeline(
            pipeline.source if pipeline.has_source else None,
            pipeline.processors,
            temp_writer
        )

        # Execute the new pipeline
        new_pipeline.process(source)

        # Iterate through all written files
        for dirpath, dirnames, filenames in os.walk(temp_directory):
            for filename in filenames:
                # Create a filename relative to the temp directory
                full_filename = os.path.normpath(
                    os.path.join(os.path.relpath(dirpath, temp_directory), filename)
                )

                # Open the temp file and yield its contents
                with open(os.path.join(temp_directory, full_filename), "rb") as file:
                    yield full_filename, file
