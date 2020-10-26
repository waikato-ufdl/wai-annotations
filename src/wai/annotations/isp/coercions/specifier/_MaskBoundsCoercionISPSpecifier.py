from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class MaskBoundsCoercionISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the mask-bounds coercion.
    """
    @classmethod
    def description(cls) -> str:
        return "Converts all annotation bounds into polygon regions"

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        if input_domain is ImageObjectDetectionDomainSpecifier:
            return ImageObjectDetectionDomainSpecifier
        else:
            raise Exception(
                f"MaskBoundsCoercion only handles the "
                f"{ImageObjectDetectionDomainSpecifier.name()} domain"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from ...coercions.component import MaskBoundsCoercion
        return MaskBoundsCoercion,
