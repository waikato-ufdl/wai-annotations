import os

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.geometry import Point, Polygon

from ....core.component.util import AnnotationFileProcessor
from ....core.stream import ThenFunction
from ....domain.image import Image
from ....domain.image.object_detection import ImageObjectDetectionInstance
from ....domain.image.object_detection.util import set_object_label, set_object_prefix
from ..configuration import COCOFile, Annotation


class FromCOCO(AnnotationFileProcessor[ImageObjectDetectionInstance]):
    """

    """
    def read_annotation_file(
            self,
            filename: str,
            then: ThenFunction[ImageObjectDetectionInstance]
    ):
        # Read in the file
        coco_file: COCOFile = COCOFile.load_json_from_file(filename)

        # Get the mapping from category ID to label
        label_lookup = {category.id: category.name for category in coco_file.categories}

        # Get a mapping from category ID to prefix
        prefix_lookup = {category.id: category.supercategory for category in coco_file.categories}

        # Create the path to the directory
        path = os.path.dirname(filename)

        # Each image yields an instance
        for image in coco_file.images:
            # Get the image associated to this entry
            image_file = os.path.join(path, image.file_name)

            # Load the image
            image_data = None
            if os.path.exists(image_file):
                with open(image_file, "rb") as file:
                    image_data = file.read()

            # Create the image info object
            image_info = Image(image.file_name, image_data, size=(image.width, image.height))

            # Collect the annotations for this image
            annotations = [annotation for annotation in coco_file.annotations if annotation.image_id == image.id]

            # Get the labels from the categories
            labels = [label_lookup[annotation.category_id] for annotation in annotations]

            # Get the prefixes from the categories
            prefixes = [prefix_lookup[annotation.category_id] for annotation in annotations]

            then(
                ImageObjectDetectionInstance(
                    image_info,
                    LocatedObjects(map(self.to_located_object, annotations, labels, prefixes)))
            )

    def read_negative_file(
            self,
            filename: str,
            then: ThenFunction[ImageObjectDetectionInstance]
    ):
        then(
            ImageObjectDetectionInstance.negative(filename)
        )

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
