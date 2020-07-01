from abc import abstractmethod
from typing import Type, Any

from ..instance import Instance, FileInfo


class DomainSpecifier:
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
    def file_type(cls) -> Type[FileInfo]:
        """
        Gets the file-representative type
        """
        pass

    @classmethod
    @abstractmethod
    def annotations_type(cls) -> Type[Any]:
        """
        Gets the annotations-representative type.
        """
        pass

    @classmethod
    def instance_class(cls) -> Type[Instance]:
        """
        Gets the instance class for this domain.
        """
        return Instance[cls.file_type(), cls.annotations_type()]
