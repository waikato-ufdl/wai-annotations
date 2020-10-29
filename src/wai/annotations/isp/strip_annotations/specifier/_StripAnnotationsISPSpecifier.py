from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class StripAnnotationsISPSpecifier(ProcessorStageSpecifier):
    """
    Specifier for the strip-annotations inline stream-processor.
    """
    @classmethod
    def description(cls) -> str:
        return "ISP which removes annotations from instances"

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        # Works in any domain
        return input_domain

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from ..component import StripAnnotations
        return StripAnnotations,
