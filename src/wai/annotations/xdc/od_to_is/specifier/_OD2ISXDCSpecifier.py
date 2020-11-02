from typing import Tuple, Type

from ....core.component import Component
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class OD2ISXDCSpecifier(ProcessorStageSpecifier):
    """
    Specifies the image object-detection -> image segmentation
    cross-domain converter.
    """
    @classmethod
    def description(cls) -> str:
        return "Converts image object-detection instances into image segmentation instances"

    @classmethod
    def domain_transfer_function(cls, input_domain: Type[DomainSpecifier]) -> Type[DomainSpecifier]:
        from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        from ....domain.image.segmentation import ImageSegmentationDomainSpecifier
        if input_domain is ImageObjectDetectionDomainSpecifier:
            return ImageSegmentationDomainSpecifier
        else:
            raise Exception("OD -> IS XDC can only handle the image object-detection domain")

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import OD2ISXDC
        return OD2ISXDC,
