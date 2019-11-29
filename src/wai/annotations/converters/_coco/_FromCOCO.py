from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.geometry import Polygon, Point

from ...coco_utils.configuration import Annotation
from ...core import ExternalFormatConverter, InternalFormat
from ...core.constants import LABEL_METADATA_KEY, PREFIX_METADATA_KEY
from ...core.external_formats import COCOExternalFormat


class FromCOCO(ExternalFormatConverter[COCOExternalFormat]):
    """
    Converter from COCO annotations to internal format.
    """
    def _convert(self, instance: COCOExternalFormat) -> InternalFormat:
        # Unpack the external format
        image_info, annotations, labels, prefixes = instance

        return image_info, LocatedObjects(map(self.to_located_object, annotations, labels, prefixes))

    def to_located_object(self, annotation: Annotation, label: str, prefix: str) -> LocatedObject:
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
                                       round(annotation.bbox[3]),
                                       **{LABEL_METADATA_KEY: label,
                                          PREFIX_METADATA_KEY: prefix})

        # Create the polygon if there is one
        points = []
        if len(annotation.segmentation) == 1:
            for index in range(0, len(annotation.segmentation[0]), 2):
                x = round(annotation.segmentation[0][index])
                y = round(annotation.segmentation[0][index + 1])

                points.append(Point(x, y))

            located_object.set_polygon(Polygon(*points))

        return located_object
