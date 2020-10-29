from typing import Dict

from ....core.component.util import JSONFileWriter, SplitSink, SplitState, ExpectsFile
from ..configuration import VGGFile, Image
from ..utils import VGGExternalFormat


class VGGWriter(
    ExpectsFile,
    JSONFileWriter[VGGExternalFormat],
    SplitSink[VGGExternalFormat]
):
    """
    Writer of VGG-format JSON files.
    """
    _split_image: Dict[str, Image] = SplitState(lambda self: {})
    _split_path: str = SplitState(lambda self: self.get_split_path(self.split_label, self.output_path))

    def consume_element_for_split(
            self,
            element: VGGExternalFormat
    ):
        # Unpack the instance
        image_info, image = element

        # Write the image
        self.write_data_file(image_info, self._split_path)

        # If the image is a negative, skip writing it
        if len(image.regions) == 0:
            return

        self._split_image[f"{image.filename}-1"] = image

    def finish_split(self):
        VGGFile(**self._split_image).save_json_to_file(
            self.get_split_path(self.split_label, self.output, True),
            self.indent
        )

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "output file to write annotations to (images are placed in same directory)"
