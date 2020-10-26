from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class BoxBoundsCoercionISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the box-bounds coercion.
    """
    @classmethod
    def description(cls) -> str:
        return "Converts all annotation bounds into box regions"

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
                f"BoxBoundsCoercion only handles the "
                f"{ImageObjectDetectionDomainSpecifier.name()} domain"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from ...coercions.component import BoxBoundsCoercion
        return BoxBoundsCoercion,
