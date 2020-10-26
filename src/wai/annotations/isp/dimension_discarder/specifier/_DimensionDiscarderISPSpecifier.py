from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class DimensionDiscarderISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the dimension-discarder.
    """
    @classmethod
    def description(cls) -> str:
        return "Removes annotations which fall outside certain size constraints"

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
                f"DimensionDiscarder only handles the "
                f"{ImageObjectDetectionDomainSpecifier.name()} domain"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from ...dimension_discarder.component import DimensionDiscarder
        return DimensionDiscarder,
