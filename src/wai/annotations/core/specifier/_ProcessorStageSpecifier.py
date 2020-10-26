from abc import abstractmethod
from typing import Type, Optional, Set

from ..domain import DomainSpecifier
from ._StageSpecifier import StageSpecifier


class ProcessorStageSpecifier(StageSpecifier):
    """
    Specifier for a conversion from one domain to another.
    """
    @classmethod
    @abstractmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        """
        Function from an input domain to an output domain. Should raise an
        exception if the input domain is not handled by the processor.
        """
        raise NotImplementedError(cls.domain_transfer_function.__qualname__)
