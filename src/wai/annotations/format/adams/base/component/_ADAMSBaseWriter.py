import os

from wai.common.file.report import save

from .....core.component.util import (
    SeparateFileWriter,
    SplitSink,
    SplitState,
    RequiresNoSplitFinalisation,
    ExpectsDirectory
)
from ...util import ADAMSExternalFormat
from ... import constants


class ADAMSBaseWriter(
    ExpectsDirectory,
    RequiresNoSplitFinalisation,
    SeparateFileWriter[ADAMSExternalFormat],
    SplitSink[ADAMSExternalFormat]
):
    # The path to write to for the split
    split_path: str = SplitState(
        lambda self: self.get_split_path(self.split_label, self.output)
    )

    @property
    def expects_file(self) -> bool:
        return False

    def consume_element_for_split(
            self,
            element: ADAMSExternalFormat
    ):
        # Unpack the instance
        image_info, report = element

        # Save the image
        self.write_data_file(image_info, self.split_path)

        # If there's no report, we're done
        if report is None:
            return

        # Format the report filename
        report_filename = f"{os.path.splitext(image_info.filename)[0]}{constants.DEFAULT_EXTENSION}"

        # Save the report
        save(report, os.path.join(self.split_path, report_filename))

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "output directory to write files to"
