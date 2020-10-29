import os

from ....core.component.util import AnnotationFileProcessor
from ....core.stream import ThenFunction
from ....domain.image import Image
from ..configuration import VGGFile, Image as JSONImage, FileAttributes
from ..utils import VGGExternalFormat


class VGGReader(AnnotationFileProcessor[VGGExternalFormat]):
    """
    Reader of VGG-format JSON files.
    """
    def read_annotation_file(
            self,
            filename: str,
            then: ThenFunction[VGGExternalFormat]
    ):
        # Read in the file
        vgg_file: VGGFile = VGGFile.load_json_from_file(filename)

        # Create the path to the directory
        path = os.path.dirname(filename)

        # Each image yields an instance
        for key in vgg_file:
            # Get the image
            image = vgg_file[key]

            # Get the image associated to this entry
            image_file = os.path.join(path, image.filename)

            # Load the image
            image_data = None
            if os.path.exists(image_file):
                with open(image_file, "rb") as file:
                    image_data = file.read()

            then(
                (
                    Image(image.filename, image_data),
                    image
                )
            )

    def read_negative_file(
            self,
            filename: str,
            then: ThenFunction[VGGExternalFormat]
    ):
        image_info = Image.from_file(filename)

        then(
            (
                image_info,
                JSONImage(
                    filename=image_info.filename,
                    size=-1,
                    file_attributes=FileAttributes(caption="", public_domain="no", image_url=""),
                    regions=[]
                )
            )
        )
