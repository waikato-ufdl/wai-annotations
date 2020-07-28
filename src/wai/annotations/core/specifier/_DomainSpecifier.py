from abc import abstractmethod
from typing import Type, TypeVar, Generic

from ..instance import Instance, FileInfo

FileType = TypeVar("FileType", bound=FileInfo)
AnnotationsType = TypeVar("AnnotationsType")


class DomainSpecifier(Generic[FileType, AnnotationsType]):
    """
    Class which specifies the internal representation of files/annotations in
    a specific domain (e.g. images, videos, etc.).
    """
    @classmethod
    @abstractmethod
    def domain_name(cls) -> str:
        """
        Gets a short descriptive name for the domain.
        """
        pass

    @classmethod
    @abstractmethod
    def instance_class(cls) -> Type[Instance[FileType, AnnotationsType]]:
        """
        Gets the instance class for this domain.
        """
        pass
