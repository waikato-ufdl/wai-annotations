from typing import Iterator

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.geometry import Polygon, Point

from ....core.component import InputConverter
from ....domain.image.object_detection import ObjectDetectionInstance
from ....domain.image.object_detection.util import set_object_label, set_object_prefix
from ..configuration import Annotation
from .._format import COCOExternalFormat


class FromCOCO(InputConverter[COCOExternalFormat, ObjectDetectionInstance]):
    """
    Converter from COCO annotations to internal format.
    """
    def convert(self, instance: COCOExternalFormat) -> Iterator[ObjectDetectionInstance]:
        # Unpack the external format
        image_info, annotations, labels, prefixes = instance

        yield ObjectDetectionInstance(image_info, LocatedObjects(map(self.to_located_object, annotations, labels, prefixes)))

    @staticmethod
    def to_located_object(annotation: Annotation, label: str, prefix: str) -> LocatedObject:
        """
        Converts an COCO annotation/label pair into a located object.

        :param annotation:  The annotation.
        :param label:       The label.
        :param prefix:      The prefix.
        :return:            The located object.
        """
        # Create the located object
        located_object = LocatedObject(round(annotation.bbox[0]),
                                       round(annotation.bbox[1]),
                                       round(annotation.bbox[2]),
                                       round(annotation.bbox[3]))
        set_object_label(located_object, label)
        set_object_prefix(located_object, prefix)

        # Create the polygon if there is one
        points = []
        if len(annotation.segmentation) == 1:
            for index in range(0, len(annotation.segmentation[0]), 2):
                x = round(annotation.segmentation[0][index])
                y = round(annotation.segmentation[0][index + 1])

                points.append(Point(x, y))

            located_object.set_polygon(Polygon(*points))

        return located_object
