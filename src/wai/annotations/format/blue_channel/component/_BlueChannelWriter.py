import os

from ....core.component.util import (
    SplitSink,
    SeparateFileWriter,
    RequiresNoSplitFinalisation,
    SplitState,
    ExpectsDirectory
)
from ....domain.image import ImageFormat
from ..util import BlueChannelFormat


class BlueChannelWriter(
    ExpectsDirectory,
    RequiresNoSplitFinalisation,
    SeparateFileWriter[BlueChannelFormat],
    SplitSink[BlueChannelFormat]
):
    """
    Writes the blue-channel format to disk.
    """
    # The output path for each split
    _split_path: str = SplitState(lambda self: self.get_split_path(self.split_label, self.output))

    def consume_element_for_split(
            self,
            element: BlueChannelFormat
    ):
        # Make sure the image file isn't a PNG
        if element.image.format is ImageFormat.PNG:
            raise Exception("Image format is PNG, so data image will clash with annotation image")

        # Write the image file to disk
        self.write_data_file(element.image, self._split_path)

        # We're finished if it's a negative image
        if element.annotations is None:
            return

        # Generate the filename for the annotation image
        annotation_filename = os.path.join(self._split_path, element.image.filename)
        annotation_filename = os.path.splitext(annotation_filename)[0] + ".png"

        # Save the annotations image
        element.annotations.save(annotation_filename)

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "the directory to write the annotation images to"
