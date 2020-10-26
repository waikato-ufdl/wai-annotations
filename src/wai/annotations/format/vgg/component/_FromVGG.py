from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image.object_detection import ImageObjectDetectionInstance
from ....domain.image.object_detection.util import set_object_label
from ..configuration import Region, PolygonShapeAttributes
from ..utils import from_polygon_shape_attributes, from_rect_shape_attributes, VGGExternalFormat


class FromVGG(
    RequiresNoFinalisation,
    ProcessorComponent[VGGExternalFormat, ImageObjectDetectionInstance]
):
    """
    Converter from VGG annotations to internal format.
    """
    def process_element(
            self,
            element: VGGExternalFormat,
            then: ThenFunction[ImageObjectDetectionInstance],
            done: DoneFunction
    ):
        # Unpack the external format
        image_info, image = element

        # Extract located objects from the JSON
        located_objects = None
        if image is not None:
            located_objects = LocatedObjects(map(self.to_located_object, image.regions))

        then(
            ImageObjectDetectionInstance(
                image_info,
                located_objects
            )
        )

    @staticmethod
    def to_located_object(region: Region) -> LocatedObject:
        """
        Converts a VGG Region configuration to a located object.

        :param region:      The region.
        :return:            The located object.
        """
        # Get the object label
        label: str = region.region_attributes.type

        # Get the shape attributes
        if isinstance(region.shape_attributes, PolygonShapeAttributes):
            x, y, width, height, polygon = from_polygon_shape_attributes(region.shape_attributes)
        else:
            x, y, width, height = from_rect_shape_attributes(region.shape_attributes)
            polygon = None

        # Create the located object
        located_object = LocatedObject(x, y, width, height)
        set_object_label(located_object, label)

        # Add the polygon if there is one
        if polygon is not None:
            located_object.set_polygon(polygon)

        return located_object
