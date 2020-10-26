from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class DiscardNegativesISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the discard-negatives ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Discards negative examples (those without annotations) from the stream"

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        # Works for all domains
        return input_domain

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from ...discard_negatives.component import DiscardNegatives
        return DiscardNegatives,
