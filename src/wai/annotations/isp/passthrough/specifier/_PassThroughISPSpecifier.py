from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class PassThroughISPSpecifier(ProcessorStageSpecifier):
    """
    Specifier for the pass-through inline stream-processor.
    """
    @classmethod
    def description(cls) -> str:
        return "Dummy ISP which has no effect on the conversion stream"

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        # Passthrough works in any domain
        return input_domain

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from ...passthrough.component import PassThrough
        return PassThrough,
