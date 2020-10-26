from abc import abstractmethod
from typing import Type, TypeVar, Generic

from ._Data import Data
from ._Instance import Instance

DataType = TypeVar("DataType", bound=Data)
AnnotationsType = TypeVar("AnnotationsType")


class DomainSpecifier(Generic[DataType, AnnotationsType]):
    """
    Class which specifies the internal representation of files/annotations in
    a specific domain (e.g. images, videos, etc.).
    """
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
        Gets a short descriptive name for the domain.
        """
        raise NotImplementedError(cls.name.__qualname__)

    @classmethod
    def description(cls) -> str:
        """
        Gets a longer description of the domain.
        """
        raise NotImplementedError(cls.description.__qualname__)

    @classmethod
    @abstractmethod
    def data_type(cls) -> Type[DataType]:
        """
        Gets the instance class for this domain.
        """
        raise NotImplementedError(cls.data_type.__qualname__)

    @classmethod
    @abstractmethod
    def annotations_type(cls) -> Type[AnnotationsType]:
        """
        The type of the annotations for this domain.
        """
        raise NotImplementedError(cls.annotations_type.__qualname__)

    @classmethod
    def instance_type(cls) -> Type[Instance[DataType, AnnotationsType]]:
        """
        The type of an instance in this domain.
        """
        raise NotImplementedError(cls.instance_type.__qualname__)
