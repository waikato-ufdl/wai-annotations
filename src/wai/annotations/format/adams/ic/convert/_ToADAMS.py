from typing import Iterator

from wai.common.cli.options import TypedOption
from wai.common.file.report import Report

from .....core.component import OutputConverter
from .....domain.image.classification import ImageClassificationInstance
from ..._format import ADAMSExternalFormat


class ToADAMS(OutputConverter[ImageClassificationInstance, ADAMSExternalFormat]):
    """
    Converter from internal format to ADAMS report-style annotations.
    """
    class_field: str = TypedOption(
        "-c", "--class-field",
        type=str,
        required=True,
        help="the report field containing the image class",
        metavar="FIELD"
    )

    def convert(self, instance: ImageClassificationInstance) -> Iterator[ADAMSExternalFormat]:
        # Create a basic report with the image class as its only field
        report = Report()
        report.set_string_value(self.class_field, instance.annotations)

        yield (instance.file_info, report)
