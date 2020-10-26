from wai.common.cli.options import TypedOption

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image import ImageFormat, ImageInstance


class ConvertImageFormat(
    RequiresNoFinalisation,
    ProcessorComponent[ImageInstance, ImageInstance]
):
    """
    Processes a stream of image-based instances, converting the
    image format to a specified type.
    """
    format = TypedOption(
        "-f", "--format",
        type=ImageFormat,
        required=True,
        metavar="FORMAT",
        help="format to convert images to"
    )

    def process_element(
            self,
            element: ImageInstance,
            then: ThenFunction[ImageInstance],
            done: DoneFunction
    ):
        then(
            type(element)(
                element.data.convert(self.format),
                element.annotations
            )
        )
