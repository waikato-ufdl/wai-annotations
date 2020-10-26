from wai.common.cli.options import TypedOption
from wai.common.file.report import Report

from .....core.component import ProcessorComponent
from .....core.stream import ThenFunction, DoneFunction
from .....core.stream.util import RequiresNoFinalisation
from .....domain.image.classification import ImageClassificationInstance
from ...util import ADAMSExternalFormat


class ToADAMS(
    RequiresNoFinalisation,
    ProcessorComponent[ImageClassificationInstance, ADAMSExternalFormat]
):
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

    def process_element(
            self,
            element: ImageClassificationInstance,
            then: ThenFunction[ADAMSExternalFormat],
            done: DoneFunction
    ):
        # Create a basic report with the image class as its only field
        report = None
        if element.annotations is not None:
            report = Report()
            report.set_string_value(self.class_field, element.annotations.label)

        then((element.data, report))
