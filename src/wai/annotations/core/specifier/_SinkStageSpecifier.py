from abc import abstractmethod
from typing import Type

from ..domain import DomainSpecifier
from ._StageSpecifier import StageSpecifier


class SinkStageSpecifier(StageSpecifier):
    """
    Class which specifies the components available to write a given format.
    """
    @classmethod
    @abstractmethod
    def domain(cls) -> Type[DomainSpecifier]:
        """
        The domain of the format.
        """
        pass
