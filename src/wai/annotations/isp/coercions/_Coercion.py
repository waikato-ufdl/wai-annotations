from abc import abstractmethod
from typing import Iterable

from wai.common.adams.imaging.locateobjects import LocatedObject

from ...core.component import InlineStreamProcessor
from ...domain.image.object_detection import ImageObjectDetectionDomainSpecifier

ObjectDetectionInstance = ImageObjectDetectionDomainSpecifier.instance_class()


class Coercion(InlineStreamProcessor[ObjectDetectionInstance]):
    """
    Base class for all coercions.
    """
    def _process_element(self, element: ObjectDetectionInstance) -> Iterable[ObjectDetectionInstance]:
        # Get the located objects from the instance
        image_info, located_objects = element

        # Process each located object
        for located_object in located_objects:
            self._process_located_object(located_object)

        return element,

    @abstractmethod
    def _process_located_object(self, located_object: LocatedObject):
        """
        Handles the processing of individual located objects.

        :param located_object:  The located object to coerce.
        """
        pass
