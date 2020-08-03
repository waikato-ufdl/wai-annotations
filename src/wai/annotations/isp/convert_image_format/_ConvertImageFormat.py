from typing import Iterable

from wai.common.cli.options import TypedOption

from ...core.component import InlineStreamProcessor
from ...core.instance import Instance
from ...domain.image import ImageFormat
from ...domain.image.object_detection import ObjectDetectionInstance
from ...domain.image.classification import ImageClassificationInstance


class ConvertImageFormat(InlineStreamProcessor[Instance]):
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

    def _process_element(self, element: Instance) -> Iterable[Instance]:
        if isinstance(element, ObjectDetectionInstance):
            yield ObjectDetectionInstance(
                element.file_info.convert(self.format),
                element.annotations
            )
        elif isinstance(element, ImageClassificationInstance):
            yield ImageClassificationInstance(
                element.file_info.convert(self.format),
                element.annotations
            )

        yield element
