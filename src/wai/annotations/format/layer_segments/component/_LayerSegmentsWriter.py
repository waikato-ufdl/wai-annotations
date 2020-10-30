import os

from ....core.component.util import (
    SeparateFileWriter,
    SplitSink,
    RequiresNoSplitFinalisation,
    ExpectsDirectory,
    SplitState
)
from ..util import LabelSeparatorMixin
from ..util import LayerSegmentsOutputFormat


class LayerSegmentsWriter(
    ExpectsDirectory,
    RequiresNoSplitFinalisation,
    LabelSeparatorMixin,
    SeparateFileWriter[LayerSegmentsOutputFormat],
    SplitSink[LayerSegmentsOutputFormat]
):
    """
    Writes the one-image-per-label format to disk.
    """
    split_path = SplitState(lambda self: self.get_split_path(self.split_label, self.output_path))

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "the directory to write the annotation images to"

    def consume_element_for_split(self, element: LayerSegmentsOutputFormat):
        self.write_data_file(element.image, self.split_path)

        # Don't write anything for negative images
        if len(element.annotations) == 0:
            return

        # Write each label image separately
        for label, annotation_image in element.annotations.items():
            # Generate the filename for the annotation image
            annotation_filename = self.format_filename_with_label(
                os.path.join(self.split_path, element.image.filename), label
            )
            annotation_filename = os.path.splitext(annotation_filename)[0] + ".png"

            # Save the image
            annotation_image.save(annotation_filename)
