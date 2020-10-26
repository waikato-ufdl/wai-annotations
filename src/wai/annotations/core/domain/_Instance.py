from abc import abstractmethod
from typing import TypeVar, Generic, Optional, Type

from ._Data import Data

DataType = TypeVar("DataType", bound=Data)
AnnotationsType = TypeVar("AnnotationsType")
ClassType = TypeVar("ClassType", bound='Instance')


class Instance(Generic[DataType, AnnotationsType]):
    """
    A single item (i.e. file) from the data-set being converted.
    """
    def __init__(self, data: DataType, annotations: Optional[AnnotationsType]):
        self._data: DataType = data
        self._annotations: Optional[AnnotationsType] = annotations

    @property
    def data(self) -> DataType:
        return self._data

    @classmethod
    @abstractmethod
    def data_type(cls) -> Type[DataType]:
        raise NotImplementedError(cls.data_type.__qualname__)

    @property
    def annotations(self) -> Optional[AnnotationsType]:
        return self._annotations

    @classmethod
    @abstractmethod
    def annotations_type(cls) -> Type[AnnotationsType]:
        raise NotImplementedError(cls.annotations_type.__qualname__)

    @property
    def is_negative(self) -> bool:
        """
        Whether this instance is a negative instance (contains no annotations).
        """
        return self.annotations is None

    @classmethod
    def negative(cls: Type[ClassType], filename: str) -> ClassType:
        """
        Creates a negative instance of this class.

        :param filename:    The image file to open.
        :return:            The negative instance.
        """
        return cls(
            cls.data_type().from_file(filename),
            None
        )

    def __iter__(self):
        yield self._data
        yield self._annotations
