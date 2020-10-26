from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class RemoveClassesISPSpecifier(ProcessorStageSpecifier):
    """
    Specifier for the remove-classes inline stream-processor.
    """
    @classmethod
    def description(cls) -> str:
        return "Removes classes from classification/image-segmentation instances"

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from ....domain.classification import Classification
        from ....domain.image.segmentation import ImageSegmentationDomainSpecifier
        if (
                input_domain is ImageSegmentationDomainSpecifier or
                input_domain.annotations_type() is Classification
        ):
            return input_domain

        raise Exception("RemovesClasses handles image segmentation and classification domains only")

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from ..component import RemoveClasses
        return RemoveClasses,
