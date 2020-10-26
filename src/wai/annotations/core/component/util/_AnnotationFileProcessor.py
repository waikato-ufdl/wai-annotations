from abc import abstractmethod
from typing import Tuple

from ...stream import ThenFunction, DoneFunction
from ...stream.util import RequiresNoFinalisation
from .._ProcessorComponent import ProcessorComponent, OutputElementType


class AnnotationFileProcessor(
    RequiresNoFinalisation,
    ProcessorComponent[Tuple[str, bool], OutputElementType]
):
    """
    Processor which reads in the annotation/negative files specified
    by a LocalFileReader.
    """
    def process_element(
            self,
            element: Tuple[str, bool],
            then: ThenFunction[OutputElementType],
            done: DoneFunction
    ):
        filename, is_negative = element
        if is_negative:
            self.read_negative_file(filename, then)
        else:
            self.read_annotation_file(filename, then)

    @abstractmethod
    def read_annotation_file(self, filename: str, then: ThenFunction[OutputElementType]):
        raise NotImplementedError(self.read_annotation_file.__qualname__)

    @abstractmethod
    def read_negative_file(self, filename: str, then: ThenFunction[OutputElementType]):
        raise NotImplementedError(self.read_negative_file.__qualname__)
