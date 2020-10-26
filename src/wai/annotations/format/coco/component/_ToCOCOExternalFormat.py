from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image.object_detection import ImageObjectDetectionInstance
from ....domain.image.object_detection.util import get_object_label, get_object_prefix
from ..util import located_object_to_annotation, COCOExternalFormat


class ToCOCOExternalFormat(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, COCOExternalFormat]
):
    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[COCOExternalFormat],
            done: DoneFunction
    ):
        image_info, located_objects = element

        # Create an empty iterable if this is a negative instance
        if located_objects is None:
            located_objects = tuple()

        then(
            (
                image_info,
                list(map(located_object_to_annotation, located_objects)),
                list(map(get_object_label, located_objects)),
                list(map(get_object_prefix, located_objects))
            )
        )
