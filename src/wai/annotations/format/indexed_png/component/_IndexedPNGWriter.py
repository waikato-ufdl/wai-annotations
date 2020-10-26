import os

from ....core.component.util import (
    SeparateFileWriter,
    SplitSink,
    RequiresNoSplitFinalisation,
    SplitState,
    ExpectsDirectory
)
from ....domain.image import ImageFormat
from ..util import IndexedPNGFormat


class IndexedPNGWriter(
    ExpectsDirectory,
    RequiresNoSplitFinalisation,
    SeparateFileWriter[IndexedPNGFormat],
    SplitSink[IndexedPNGFormat]
):
    """
    Writes the indexed-PNG format to disk.
    """
    # The path to write to for each split
    _split_path: str = SplitState(lambda self: self.get_split_path(self.split_label, self.output))

    def consume_element_for_split(
            self,
            element: IndexedPNGFormat
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
