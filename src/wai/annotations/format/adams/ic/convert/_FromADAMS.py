from typing import Iterator

from wai.common.cli.options import TypedOption

from .....core.component import InputConverter
from .....domain.image.classification import ImageClassificationInstance
from ..._format import ADAMSExternalFormat


class FromADAMS(InputConverter[ADAMSExternalFormat, ImageClassificationInstance]):
    """
    Converter from ADAMS report-style image classification instance to internal format.
    """
    class_field: str = TypedOption(
        "-c", "--class-field",
        type=str,
        required=True,
        help="the report field containing the image class",
        metavar="FIELD"
    )

    def convert(self, instance: ADAMSExternalFormat) -> Iterator[ImageClassificationInstance]:
        # Get the class from the report
        class_value = instance[1].get_string_value(self.class_field)

        # Raise an error if no class value was found
        if class_value is None:
            raise Exception(f"Report for {instance[0].filename} has no field '{self.class_field}'")

        yield ImageClassificationInstance(
            instance[0],
            instance[1].get_string_value(self.class_field)
        )
