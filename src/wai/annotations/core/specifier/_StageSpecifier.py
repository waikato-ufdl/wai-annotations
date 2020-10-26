from abc import ABC, abstractmethod
from typing import Tuple, Type

from ..component import Component


class StageSpecifier(ABC):
    """
    Base class for classes which specify the components of a plugin stage.
    """
    @classmethod
    @abstractmethod
    def description(cls) -> str:
        """
        A short description of the functionality the plugin component provides.
        """
        raise NotImplementedError(cls.description.__qualname__)

    @classmethod
    @abstractmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        """
        The components which make up the stage, in order of application.
        """
        raise NotImplementedError(cls.components.__qualname__)
