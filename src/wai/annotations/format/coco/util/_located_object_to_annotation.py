from wai.common.adams.imaging.locateobjects import LocatedObject

from ..configuration import Annotation


def located_object_to_annotation(located_object: LocatedObject) -> Annotation:
    """
    Converts the located object into a COCO annotation.

    :param located_object:      The located object to convert.
    :return:                    The COCO annotation object.
    """
    # Get the object's polygon if it has one
    polygon = []
    if located_object.has_polygon():
        for point in located_object.get_polygon():
            polygon.append(float(point.x))
            polygon.append(float(point.y))

    # Calculate the area of the annotation
    if located_object.has_polygon():
        area = located_object.get_polygon().area()
    else:
        area = float(located_object.get_rectangle().area())

    return Annotation(id=0, image_id=0, category_id=0,  # Will be calculated at write-time
                      segmentation=[polygon] if len(polygon) > 0 else [],
                      area=area,
                      bbox=[float(located_object.x), float(located_object.y),
                            float(located_object.width), float(located_object.height)],
                      iscrowd=0)
