import os
from typing import Iterable

from ....core.component import SeparateFileWriter
from ....domain.image import ImageInfo, ImageFormat
from .._format import BlueChannelFormat


class BlueChannelWriter(SeparateFileWriter[BlueChannelFormat]):
    """
    Writes the blue-channel format to disk.
    """
    def write_annotations_only(self, instances: Iterable[BlueChannelFormat], path: str):
        for instance in instances:
            # Don't write anything for negative images
            if instance.annotations is None:
                continue

            # Make sure the image file isn't a PNG
            if instance.image.format is ImageFormat.PNG:
                raise Exception("Image format is PNG, so data image will clash with annotation image")

            # Generate the filename for the annotation image
            annotation_filename = os.path.join(path, instance.image.filename)
            annotation_filename = os.path.splitext(annotation_filename)[0] + ".png"

            instance.annotations.save(annotation_filename)

    @classmethod
    def output_help_text(cls) -> str:
        return "the directory to write the annotation images to"

    def expects_file(self) -> bool:
        return False

    def extract_file_info_from_external_format(self, instance: BlueChannelFormat) -> ImageInfo:
        return instance.image
