from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class ConvertImageFormatISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the convert-image-format ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Converts images from one format to another"

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from ....domain.image import Image
        if input_domain.data_type() is Image:
            return input_domain
        else:
            raise Exception(f"ConvertImageFormat only handles the image-based domains")

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from ...convert_image_format.component import ConvertImageFormat
        return ConvertImageFormat,
