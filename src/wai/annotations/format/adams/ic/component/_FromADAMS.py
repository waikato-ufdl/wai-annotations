from wai.common.cli.options import TypedOption

from .....core.component import ProcessorComponent
from .....core.stream import ThenFunction, DoneFunction
from .....core.stream.util import RequiresNoFinalisation
from .....domain.classification import Classification
from .....domain.image.classification import ImageClassificationInstance
from ...util import ADAMSExternalFormat


class FromADAMS(
    RequiresNoFinalisation,
    ProcessorComponent[ADAMSExternalFormat, ImageClassificationInstance]
):
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

    def process_element(
            self,
            element: ADAMSExternalFormat,
            then: ThenFunction[ImageClassificationInstance],
            done: DoneFunction
    ):
        # Get the class from the report (if there is one)
        class_value = (
            element[1].get_string_value(self.class_field)
            if element[1] is not None
            else None
        )

        # Create a classification from the class string if found
        classification = (
            Classification(class_value)
            if class_value is not None
            else None
        )

        then(
            ImageClassificationInstance(
                element[0],
                classification
            )
        )
