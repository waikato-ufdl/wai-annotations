from abc import abstractmethod

from wai.common.adams.imaging.locateobjects import LocatedObject

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier

ObjectDetectionInstance = ImageObjectDetectionDomainSpecifier.instance_type()


class Coercion(
    RequiresNoFinalisation,
    ProcessorComponent[ObjectDetectionInstance, ObjectDetectionInstance]
):
    """
    Base class for all coercions.
    """
    def process_element(
            self,
            element: ObjectDetectionInstance,
            then: ThenFunction[ObjectDetectionInstance],
            done: DoneFunction
    ):
        # Get the located objects from the instance
        image_info, located_objects = element

        # Process each located object
        if located_objects is not None:
            for located_object in located_objects:
                self._process_located_object(located_object)

        then(element)

    @abstractmethod
    def _process_located_object(self, located_object: LocatedObject):
        """
        Handles the processing of individual located objects.

        :param located_object:  The located object to coerce.
        """
        pass
