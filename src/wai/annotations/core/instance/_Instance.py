from abc import abstractproperty
from typing import TypeVar, Generic

from ._FileInfo import FileInfo

FileType = TypeVar("FileType", bound=FileInfo)
AnnotationsType = TypeVar("AnnotationsType")


class Instance(Generic[FileType, AnnotationsType]):
    """
    A single item (i.e. file) from the data-set being converted.
    """
    def __init__(self, file_info: FileType, annotations: AnnotationsType):
        self._file_info: FileType = file_info
        self._annotations: AnnotationsType = annotations

    @property
    def file_info(self) -> FileType:
        return self._file_info

    @property
    def annotations(self) -> AnnotationsType:
        return self._annotations

    @abstractproperty
    def is_negative(self) -> bool:
        """
        Whether this instance is a negative instance (contains no annotations).
        """
        pass

    def __iter__(self):
        yield self.file_info
        yield self.annotations
